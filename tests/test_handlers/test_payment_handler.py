from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from graphql_client import TransactionFlowStrategyEnum
from nimara_stripe.api.stripe.app import app
from tests.test_stripe.stripe_mock import (
    FakePaymentIntent,
    FakeTaxCalculation,
    LineItem,
    LineItemsData,
    Money,
)

pytestmark = pytest.mark.anyio

saleor_client = TestClient(
    app,
    headers={
        "Saleor-Domain": "example.saleor.com",
        "Saleor-Api-Url": "https://example.com/graphql",
        "Saleor-Signature": "sig",
        "Saleor-Event": "event",
    },
)
stripe_client = TestClient(app)


@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_payment_gateway_initialize_session(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    stripe_config,
    payment_gateway_initialize_session_event,
):
    mocked_get_stripe_channel_config.return_value = stripe_config

    response = saleor_client.post(
        "/payment/gateway",
        json=payment_gateway_initialize_session_event.model_dump(),
    )

    assert response.status_code == 200
    assert response.json() == {"data": {"publishableKey": "test_stripe_pub_key_1"}}


@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_saleor_config")
async def test_payment_gateway_initialize_session_missing_channel_settings(
    mock_get_saleor_config,
    mocked_verify_webhook_signature,
    saleor_config_data,
    payment_gateway_initialize_session_event,
):
    test_body = payment_gateway_initialize_session_event

    assert (
        test_body.source_object.channel.slug
        not in saleor_config_data.stripe_configurations_for_channels
    )

    mock_get_saleor_config.return_value = saleor_config_data

    response = saleor_client.post(
        "/payment/gateway",
        json=test_body.model_dump(),
    )

    assert response.status_code == 422


@patch("nimara_stripe.api.stripe.endpoints.stripe.PaymentIntent.create")
@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_transaction_initialize_session(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    mocker_intent_create,
    mocker,
    stripe_config,
    transaction_initialize_session_event,
):
    test_body = transaction_initialize_session_event
    test_body.action.action_type = TransactionFlowStrategyEnum.AUTHORIZATION
    test_body.action.amount = 10.99
    test_body.action.currency = "USD"

    fake_payment_intent = FakePaymentIntent(
        id="fake_payment_intent_id",
        amount=1099,
        currency="USD",
        status="succeeded",
        client_secret="client_secret",
        created=datetime.now().isoformat(),
        cancellation_reason="",
        description="",
        last_payment_error=None,
    )
    mocker_intent_create.return_value = fake_payment_intent
    mocked_get_stripe_channel_config.return_value = stripe_config

    response = saleor_client.post(
        "/payment/initialize-session",
        json=test_body.model_dump(),
    )

    assert response.json() == {
        "pspReference": fake_payment_intent.id,
        "result": "AUTHORIZATION_SUCCESS",
        "amount": "10.99",
        "message": "",
        "data": {
            "paymentIntent": {
                "clientSecret": fake_payment_intent.client_secret,
                "publishableKey": "test_stripe_pub_key_1",
            },
            "time": fake_payment_intent.created,
            "externalUrl": f"https://dashboard.stripe.com/payments/{fake_payment_intent.id}",
        },
    }

    mocker_intent_create.assert_called_once_with(
        amount=1099,
        currency="USD",
        capture_method="manual",
        key="value",
        metadata={
            "transactionId": test_body.transaction.id,
            "channelId": test_body.source_object.channel.id,
            "channelSlug": test_body.source_object.channel.slug,
            "saleorDomain": "example.saleor.com",
        },
    )


@patch("nimara_stripe.api.stripe.endpoints.stripe.PaymentIntent.retrieve")
@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_transaction_process_session_without_additional_data(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    mocker_intent_retrieve,
    mocker,
    stripe_config,
    transaction_process_session_event,
):
    test_body = transaction_process_session_event
    test_body.data = {}
    test_body.action.amount = 10.99
    test_body.action.currency = "USD"
    test_body.action.action_type = TransactionFlowStrategyEnum.AUTHORIZATION

    fake_payment_intent = FakePaymentIntent(
        id="fake_payment_intent_id",
        amount=1099,
        currency="USD",
        status="succeeded",
        client_secret="client_secret",
        created=datetime.now().isoformat(),
        cancellation_reason="",
        description="",
        last_payment_error=None,
    )

    mocked_get_stripe_channel_config.return_value = stripe_config

    mocker_intent_retrieve.return_value = fake_payment_intent

    response = saleor_client.post(
        "/payment/process-session",
        json=test_body.model_dump(),
    )

    assert response.json() == {
        "pspReference": fake_payment_intent.id,
        "result": "AUTHORIZATION_SUCCESS",
        "amount": "10.99",
        "message": "",
        "data": {
            "paymentIntent": {
                "clientSecret": fake_payment_intent.client_secret,
                "publishableKey": "test_stripe_pub_key_1",
            },
            "time": fake_payment_intent.created,
            "externalUrl": f"https://dashboard.stripe.com/payments/{fake_payment_intent.id}",
        },
    }

    mocker_intent_retrieve.assert_called_once_with(
        test_body.transaction.psp_reference,
    )


@patch("nimara_stripe.api.stripe.endpoints.stripe.PaymentIntent.modify")
@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_transaction_process_session_with_additional_data(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    mocker_intent_modify,
    mocker,
    stripe_config,
    transaction_process_session_event,
):
    test_body = transaction_process_session_event
    test_body.action.amount = 10.99
    test_body.action.currency = "USD"
    test_body.action.action_type = TransactionFlowStrategyEnum.AUTHORIZATION

    fake_payment_intent = FakePaymentIntent(
        id="fake_payment_intent_id",
        amount=1099,
        currency="USD",
        status="requires_action",
        client_secret="client_secret",
        created=datetime.now().isoformat(),
        cancellation_reason="",
        description="",
        last_payment_error=None,
    )

    mocker_intent_modify.return_value = fake_payment_intent
    mocked_get_stripe_channel_config.return_value = stripe_config

    response = saleor_client.post(
        "/payment/process-session",
        json=test_body.model_dump(),
    )

    assert response.json() == {
        "pspReference": fake_payment_intent.id,
        "result": "AUTHORIZATION_ACTION_REQUIRED",
        "amount": "10.99",
        "message": "",
        "data": {
            "paymentIntent": {
                "clientSecret": fake_payment_intent.client_secret,
                "publishableKey": "test_stripe_pub_key_1",
            },
            "time": fake_payment_intent.created,
            "externalUrl": f"https://dashboard.stripe.com/payments/{fake_payment_intent.id}",
        },
    }

    mocker_intent_modify.assert_called_once_with(
        test_body.transaction.psp_reference,
        amount=1099,
        currency="USD",
        capture_method="manual",
        metadata={
            "transactionId": test_body.transaction.id,
            "channelId": test_body.source_object.channel.id,
            "channelSlug": test_body.source_object.channel.slug,
            "saleorDomain": "example.saleor.com",
        },
        info="processing step",
    )


@patch("nimara_stripe.api.stripe.endpoints.stripe.PaymentIntent.capture")
@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_transaction_charge_requested(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    mocker_intent_capture,
    stripe_config,
    transaction_charge_requested_event,
):
    fake_payment_intent = FakePaymentIntent(
        id="fake_payment_intent_id",
        amount=1099,
        currency="USD",
        status="succeeded",
        client_secret="client_secret",
        created=datetime.now().isoformat(),
        cancellation_reason="",
        description="",
        last_payment_error=None,
    )
    mocker_intent_capture.return_value = fake_payment_intent
    mocked_get_stripe_channel_config.return_value = stripe_config

    response = saleor_client.post(
        "/payment/charge",
        json=transaction_charge_requested_event.model_dump(),
    )

    assert response.json() == {
        "pspReference": fake_payment_intent.id,
        "result": "CHARGE_SUCCESS",
        "amount": "10.99",
        "externalUrl": f"https://dashboard.stripe.com/payments/{fake_payment_intent.id}",
    }

    mocker_intent_capture.assert_called_once_with(
        intent=transaction_charge_requested_event.transaction.psp_reference,
        amount_to_capture=30000,
    )


@patch("nimara_stripe.api.stripe.endpoints.stripe.PaymentIntent.cancel")
@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_transaction_cancel_requested(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    mocker_intent_cancel,
    stripe_config,
    transaction_cancellation_requested_event,
):
    fake_payment_intent = FakePaymentIntent(
        id="fake_payment_intent_id",
        amount=1099,
        currency="USD",
        status="succeeded",
        client_secret="client_secret",
        created=datetime.now().isoformat(),
        cancellation_reason="",
        description="",
        last_payment_error=None,
    )
    mocker_intent_cancel.return_value = fake_payment_intent
    mocked_get_stripe_channel_config.return_value = stripe_config

    response = saleor_client.post(
        "/payment/cancel",
        json=transaction_cancellation_requested_event.model_dump(),
    )

    assert response.json() == {
        "pspReference": fake_payment_intent.id,
    }

    mocker_intent_cancel.assert_called_once_with(
        intent=transaction_cancellation_requested_event.transaction.psp_reference
    )


@patch("nimara_stripe.api.stripe.endpoints.stripe.Refund.create")
@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_transaction_refund_requested(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    mocker_intent_refund,
    stripe_config,
    transaction_refund_requested_event,
):
    fake_payment_intent = FakePaymentIntent(
        id="fake_payment_intent_id",
        amount=1099,
        currency="USD",
        status="succeeded",
        client_secret="client_secret",
        created=datetime.now().isoformat(),
        cancellation_reason="",
        description="",
        last_payment_error=None,
    )
    mocker_intent_refund.return_value = fake_payment_intent
    mocked_get_stripe_channel_config.return_value = stripe_config

    response = saleor_client.post(
        "/payment/refund",
        json=transaction_refund_requested_event.model_dump(),
    )

    assert response.json() == {
        "pspReference": transaction_refund_requested_event.transaction.psp_reference,
        "result": "REFUND_SUCCESS",
        "amount": "10.99",
        "externalUrl": f"https://dashboard.stripe.com/payments/{transaction_refund_requested_event.transaction.psp_reference}",
    }

    mocker_intent_refund.assert_called_once_with(
        payment_intent=transaction_refund_requested_event.transaction.psp_reference,
        amount=18000,
    )


@patch("nimara_stripe.api.stripe.endpoints.stripe.tax.Calculation.create")
@patch("nimara_stripe.services.saleor.auth.verify_webhook_signature")
@patch("nimara_stripe.api.stripe.endpoints.get_stripe_channel_config")
async def test_calculate_tax(
    mocked_get_stripe_channel_config,
    mocked_verify_webhook_signature,
    mocker_tax_calculation,
    saleor_test_calculate_tax_event,
    stripe_config,
):
    fake_tax_calculation = FakeTaxCalculation(
        amount_total=124230,
        shipping_cost=Money(
            amount=1000,
            amount_tax=230,
        ),
        currency="PLN",
        line_items=LineItemsData(data=[LineItem(amount=100000, amount_tax=23000)]),
    )
    mocker_tax_calculation.return_value = fake_tax_calculation
    mocked_get_stripe_channel_config.return_value = stripe_config

    response = saleor_client.post(
        "/payment/calculate-tax",
        json=saleor_test_calculate_tax_event.model_dump(),
    )

    assert response.json() == {
        "shipping_tax_rate": "23.00",
        "shipping_price_gross_amount": "12.30",
        "shipping_price_net_amount": "10.00",
        "lines": [
            {
                "tax_rate": "23.00",
                "total_gross_amount": "1230.00",
                "total_net_amount": "1000.00",
            }
        ],
    }

    mocker_tax_calculation.assert_called_once_with(
        currency="PLN",
        customer_details={
            "address": {
                "line1": "Street address 1",
                "line2": "Street address 2",
                "city": "Warsaw",
                "postal_code": "00-001",
                "country": "PL",
                "state": "",
            },
            "address_source": "shipping",
        },
        line_items=[{"amount": 100000, "quantity": 1, "reference": "testSku"}],
        shipping_cost={"amount": 1000},
        expand=["line_items"],
    )


@patch("nimara_stripe.api.stripe.endpoints.get_configs_from_domain_settings")
@patch("nimara_stripe.api.stripe.endpoints.validate_stripe_webhook")
@patch("nimara_stripe.api.stripe.endpoints.SaleorClient.transaction_event_report")
async def test_stripe_webhook(
    mock_transaction_event_report,
    mock_validate_stripe_webhook,
    mock_get_configs_from_domain_settings,
    saleor_config_data,
    stripe_config,
    stripe_webhook_payment_intent_created_body,
):
    mock_get_configs_from_domain_settings.return_value = (
        saleor_config_data,
        stripe_config,
    )

    response = stripe_client.post(
        "/payment/webhook",
        json=stripe_webhook_payment_intent_created_body,
        headers={"stripe-signature": "test_sig"},
    )

    assert response.json() == "OK"

    mock_transaction_event_report.assert_called()

    _, kwargs = mock_transaction_event_report.call_args
    assert kwargs["type"] == "CHARGE_ACTION_REQUIRED"


@patch("nimara_stripe.api.stripe.endpoints.get_configs_from_domain_settings")
@patch("nimara_stripe.api.stripe.endpoints.validate_stripe_webhook")
@patch("nimara_stripe.api.stripe.endpoints.SaleorClient.transaction_event_report")
async def test_stripe_webhook_missing_channel_settings(
    mock_transaction_event_report,
    mock_validate_stripe_webhook,
    mock_get_configs_from_domain_settings,
    saleor_config_data,
    stripe_webhook_payment_intent_created_body,
):
    mock_get_configs_from_domain_settings.return_value = (
        saleor_config_data,
        None,
    )

    response = stripe_client.post(
        "/payment/webhook",
        json=stripe_webhook_payment_intent_created_body,
        headers={"stripe-signature": "test_sig"},
    )

    assert response.status_code == 422
    mock_transaction_event_report.assert_not_called()


@patch("nimara_stripe.api.stripe.endpoints.get_configs_from_domain_settings")
@patch("nimara_stripe.api.stripe.endpoints.validate_stripe_webhook")
@patch("nimara_stripe.api.stripe.endpoints.SaleorClient.transaction_event_report")
async def test_stripe_webhook_without_proper_metadata(
    mock_transaction_event_report,
    mock_validate_stripe_webhook,
    mock_get_configs_from_domain_settings,
    saleor_config_data,
    stripe_webhook_payment_intent_created_body,
):
    stripe_webhook_payment_intent_created_body["data"]["object"]["metadata"] = {}

    response = stripe_client.post(
        "/payment/webhook",
        json=stripe_webhook_payment_intent_created_body,
        headers={"stripe-signature": "test_sig"},
    )

    assert response.status_code == 200
    mock_get_configs_from_domain_settings.assert_not_called()
    mock_transaction_event_report.assert_not_called()
