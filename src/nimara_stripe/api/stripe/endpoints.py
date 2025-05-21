from datetime import datetime
from typing import Annotated, Any, cast

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from saleor_sdk.marina.exceptions import InvalidSaleorDomain

from graphql_client import (
    CalculateTaxesEventCalculateTaxes,
    Money,
    PaymentGatewayInitializeSessionEvent,
    TransactionCancelationRequestedEvent,
    TransactionChargeRequestedEvent,
    TransactionEventTypeEnum,
    TransactionFlowStrategyEnum,
    TransactionInitializeSessionEvent,
    TransactionProcessSessionEvent,
    TransactionRefundRequestedEvent,
)
from nimara_stripe.api.stripe.utils import (
    prepare_saleor_base_response_data,
    prepare_saleor_response_data,
    prepare_stripe_data,
)
from nimara_stripe.services.saleor.auth import get_saleor_domain, verify_saleor_webhook
from nimara_stripe.services.saleor.client import SaleorClient
from nimara_stripe.services.saleor.config import (
    StripeConfig,
    StripeSaleorConfigData,
    StripeSaleorConfigProvider,
)
from nimara_stripe.services.saleor.utils import get_saleor_url_parts
from nimara_stripe.services.stripe.auth import (
    get_stripe_signature,
    validate_stripe_webhook,
)
from nimara_stripe.services.stripe.currencies import (
    get_saleor_amount_from_stripe_amount,
    get_stripe_amount_from_saleor_money,
)
from nimara_stripe.services.stripe.enum import CaptureMethodEnum
from nimara_stripe.services.stripe.utils import get_result
from nimara_stripe.services.stripe.webhook_utils import handle_payment_intent_event
from nimara_stripe.utils.helpers import get_logger

LOGGER = get_logger()


router = APIRouter()


async def get_stripe_channel_config(channel_slug: str, saleor_api_url: str) -> "StripeConfig":
    config = await get_saleor_config(saleor_api_url)
    stripe_channel_config = config.get_stripe_config_for_channel(channel_slug)

    if stripe_channel_config is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Configuration for '{channel_slug}' not found.",
        )
    stripe.api_key = stripe_channel_config.stripe_secret_key

    return stripe_channel_config


async def get_saleor_config(saleor_api_url: str) -> "StripeSaleorConfigData":
    saleor_url_parts = get_saleor_url_parts(saleor_api_url)
    saleor_provider = StripeSaleorConfigProvider()
    try:
        saleor_config = await saleor_provider.get_by_saleor_domain(saleor_url_parts.domain)
    except InvalidSaleorDomain:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Configuration for '{saleor_url_parts.domain}' not found.",
        )
    return saleor_config


@router.post("/gateway")
async def payment_gateway_initialize_session(
    request: Request,
    _: Annotated[None, Depends(verify_saleor_webhook)],
    event: PaymentGatewayInitializeSessionEvent,
) -> dict[str, dict[str, str]]:
    stripe_channel_config = await get_stripe_channel_config(
        event.source_object.channel.slug, request.headers.get("saleor-api-url", "")
    )

    return {"data": {"publishableKey": stripe_channel_config.stripe_pub_key}}


@router.post("/initialize-session")
async def transaction_initialize_session(
    request: Request,
    _: Annotated[None, Depends(verify_saleor_webhook)],
    saleor_domain: Annotated[str, Depends(get_saleor_domain)],
    event: TransactionInitializeSessionEvent,
) -> dict[str, Any]:
    stripe_channel_config = await get_stripe_channel_config(
        event.source_object.channel.slug, request.headers.get("saleor-api-url", "")
    )

    additional_data = event.data if event.data else {}
    additional_metadata = additional_data.get("metadata", {})
    payment_intent: stripe.PaymentIntent = stripe.PaymentIntent.create(
        **additional_data,
        amount=get_stripe_amount_from_saleor_money(
            Money(
                amount=event.action.amount,
                currency=event.action.currency,
            )
        ),
        currency=event.action.currency,
        capture_method=(
            CaptureMethodEnum.AUTOMATIC.value
            if event.action.action_type == TransactionFlowStrategyEnum.CHARGE
            else CaptureMethodEnum.MANUAL.value
        ),
        metadata={
            **additional_metadata,
            "transactionId": event.transaction.id,
            "channelId": event.source_object.channel.id,
            "channelSlug": event.source_object.channel.slug,
            "saleorDomain": saleor_domain,
        },
    )
    stripe_result = payment_intent.status
    result = get_result(event.action.action_type.value, stripe_result)

    return {
        "pspReference": payment_intent.id,
        "result": result,
        "amount": get_saleor_amount_from_stripe_amount(
            amount=payment_intent.amount, currency=payment_intent.currency
        ),
        "message": (
            payment_intent.last_payment_error.code if payment_intent.last_payment_error else ""
        ),
        "data": {
            "paymentIntent": {
                "clientSecret": payment_intent.client_secret,
                "publishableKey": stripe_channel_config.stripe_pub_key,
            },
            "time": payment_intent.created,
            "externalUrl": f"https://dashboard.stripe.com/payments/{payment_intent.id}",
        },
    }


@router.post("/process-session")
async def transaction_process_session(
    request: Request,
    _: Annotated[None, Depends(verify_saleor_webhook)],
    saleor_domain: Annotated[str, Depends(get_saleor_domain)],
    event: TransactionProcessSessionEvent,
) -> dict[str, Any]:
    stripe_channel_config = await get_stripe_channel_config(
        event.source_object.channel.slug, request.headers.get("saleor-api-url", "")
    )
    payment_intent: stripe.PaymentIntent
    if event.data:
        additional_metadata = event.data.get("metadata", {})
        update_data = {
            **event.data,
            "amount": get_stripe_amount_from_saleor_money(
                Money(
                    amount=event.action.amount,
                    currency=event.action.currency,
                )
            ),
            "currency": event.action.currency,
            "capture_method": (
                CaptureMethodEnum.AUTOMATIC.value
                if event.action.action_type == TransactionFlowStrategyEnum.CHARGE
                else CaptureMethodEnum.MANUAL.value
            ),
            "metadata": {
                **additional_metadata,
                "transactionId": event.transaction.id,
                "channelId": event.source_object.channel.id,
                "channelSlug": event.source_object.channel.slug,
                "saleorDomain": saleor_domain,
            },
        }
        payment_intent = stripe.PaymentIntent.modify(
            event.transaction.psp_reference, **update_data
        )
    else:
        payment_intent = stripe.PaymentIntent.retrieve(event.transaction.psp_reference)

    stripe_result = payment_intent.status
    result = get_result(event.action.action_type.value, stripe_result)

    return {
        "pspReference": payment_intent.id,
        "result": result,
        "amount": get_saleor_amount_from_stripe_amount(
            amount=payment_intent.amount, currency=payment_intent.currency
        ),
        "message": (
            payment_intent.last_payment_error.code if payment_intent.last_payment_error else ""
        ),
        "data": {
            "paymentIntent": {
                "clientSecret": payment_intent.client_secret,
                "publishableKey": stripe_channel_config.stripe_pub_key,
            },
            "time": payment_intent.created,
            "externalUrl": f"https://dashboard.stripe.com/payments/{payment_intent.id}",
        },
    }


@router.post("/charge")
async def transaction_charge_requested(
    request: Request,
    _: Annotated[None, Depends(verify_saleor_webhook)],
    event: TransactionChargeRequestedEvent,
) -> dict[str, Any]:
    if (
        event.transaction is None
        or event.transaction.source_object is None
        or event.action.amount is None
    ):
        raise ValueError("Invalid event: transaction, source_object, or amount is None")

    await get_stripe_channel_config(
        event.transaction.source_object.channel.slug,
        request.headers.get("saleor-api-url", ""),
    )

    payment_intent = stripe.PaymentIntent.capture(
        intent=event.transaction.psp_reference,
        amount_to_capture=get_stripe_amount_from_saleor_money(
            Money(
                amount=event.action.amount,
                currency=event.action.currency,
            )
        ),
    )

    stripe_result = payment_intent.status
    result = get_result(event.action.action_type.value, stripe_result)

    if result in ("CHARGE_SUCCESS", "CHARGE_FAILURE"):
        resp_data = {
            "pspReference": payment_intent.id,
            "result": result,
            "amount": get_saleor_amount_from_stripe_amount(
                amount=payment_intent.amount, currency=payment_intent.currency
            ),
            "externalUrl": f"https://dashboard.stripe.com/payments/{payment_intent.id}",
        }
    else:
        resp_data = {
            "pspReference": payment_intent.id,
        }
    return resp_data


@router.post("/cancel")
async def transaction_cancel_requested(
    request: Request,
    _: Annotated[None, Depends(verify_saleor_webhook)],
    event: TransactionCancelationRequestedEvent,
) -> dict[str, Any]:
    if event.transaction is None or event.transaction.source_object is None:
        raise ValueError("Invalid event: transaction or source_object is None")

    await get_stripe_channel_config(
        event.transaction.source_object.channel.slug,
        request.headers.get("saleor-api-url", ""),
    )

    payment_intent = stripe.PaymentIntent.cancel(intent=event.transaction.psp_reference)

    if payment_intent.status == "canceled":
        resp_data = {
            "pspReference": payment_intent.id,
            "result": TransactionEventTypeEnum.CANCEL_SUCCESS,
            "amount": get_saleor_amount_from_stripe_amount(
                amount=payment_intent.amount, currency=payment_intent.currency
            ),
            "externalUrl": f"https://dashboard.stripe.com/payments/{payment_intent.id}",
        }
    else:
        resp_data = {
            "pspReference": payment_intent.id,
        }
    return resp_data


@router.post("/refund")
async def transaction_refund_requested(
    request: Request,
    _: Annotated[None, Depends(verify_saleor_webhook)],
    event: TransactionRefundRequestedEvent,
) -> dict[str, Any]:
    if (
        event.transaction is None
        or event.transaction.source_object is None
        or event.action.amount is None
    ):
        raise ValueError("Invalid event: transaction, source_object, or amount is None")
    await get_stripe_channel_config(
        event.transaction.source_object.channel.slug,
        request.headers.get("saleor-api-url", ""),
    )

    refund = stripe.Refund.create(
        payment_intent=event.transaction.psp_reference,
        amount=get_stripe_amount_from_saleor_money(
            Money(
                amount=event.action.amount,
                currency=event.action.currency,
            )
        ),
    )

    if refund.status == "succeeded":
        resp_data = {
            "pspReference": event.transaction.psp_reference,
            "result": TransactionEventTypeEnum.REFUND_SUCCESS,
            "amount": get_saleor_amount_from_stripe_amount(
                amount=refund.amount, currency=refund.currency
            ),
            "externalUrl": f"https://dashboard.stripe.com/payments/{event.transaction.psp_reference}",
        }
    else:
        resp_data = {
            "pspReference": event.transaction.psp_reference,
        }
    return resp_data


async def get_configs_from_domain_settings(
    channel_slug: str, saleor_domain: str
) -> "tuple[StripeSaleorConfigData, StripeConfig | None]":
    config_provider = StripeSaleorConfigProvider()
    saleor_config = await config_provider.get_by_saleor_domain(saleor_domain)

    stripe_channel_config = saleor_config.get_stripe_config_for_channel(channel_slug)
    return saleor_config, stripe_channel_config


@router.post("/webhook")
async def stripe_webhook(
    request: Request, stripe_signature: Annotated[str, Depends(get_stripe_signature)]
) -> str:
    event_data = await request.json()

    saleor_domain = event_data["data"]["object"]["metadata"].get("saleorDomain")
    channel_slug = event_data["data"]["object"]["metadata"].get("channelSlug")
    if not saleor_domain or not channel_slug:
        # We should consider PaymentIntents without required Saleor data
        # as the payments placed with another sale channels than Saleor.
        return "OK"

    saleor_config, stripe_channel_config = await get_configs_from_domain_settings(
        event_data["data"]["object"]["metadata"]["channelSlug"],
        saleor_domain,
    )

    if not (saleor_config and stripe_channel_config):
        LOGGER.warning("No config data found for channel")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No config data found!",
        )

    stripe.api_key = stripe_channel_config.stripe_secret_key

    await validate_stripe_webhook(request, stripe_signature, stripe_channel_config, stripe)

    saleor_client = SaleorClient(
        saleor_url=f"https://{saleor_domain}", api_key=saleor_config.auth_token
    )
    event = stripe.Event.construct_from(event_data, stripe.api_key)

    payment_intent: stripe.PaymentIntent = cast(stripe.PaymentIntent, event.data.object)
    event_data = await handle_payment_intent_event(event)

    await saleor_client.transaction_event_report(
        transaction_id=payment_intent["metadata"]["transactionId"],
        amount=get_saleor_amount_from_stripe_amount(
            amount=payment_intent["amount"], currency=payment_intent["currency"]
        ),
        message=(
            payment_intent.last_payment_error.code if payment_intent.last_payment_error else ""
        ),
        available_actions=event_data["available_actions"],
        external_url=f"https://dashboard.stripe.com/payments/{payment_intent['id']}",
        psp_reference=payment_intent["id"],
        time=datetime.now().isoformat(),
        type=event_data["type"],
    )
    return "OK"


@router.post("/calculate-tax")
async def calculate_tax(
    request: Request,
    _: Annotated[None, Depends(verify_saleor_webhook)],
    event: CalculateTaxesEventCalculateTaxes,
) -> dict[str, Any]:
    await get_stripe_channel_config(
        event.tax_base.channel.slug, request.headers.get("saleor-api-url", "")
    )

    resp_data = prepare_saleor_base_response_data(event)
    if not event.tax_base.address or event.tax_base.shipping_price.amount <= 0:
        return resp_data

    shipping_cost, line_items = prepare_stripe_data(event)

    result = stripe.tax.Calculation.create(
        currency=event.tax_base.currency,
        customer_details={
            "address": {
                "line1": event.tax_base.address.street_address_1,
                "line2": event.tax_base.address.street_address_2,
                "city": event.tax_base.address.city,
                "postal_code": event.tax_base.address.postal_code,
                "country": event.tax_base.address.country.code,
                "state": event.tax_base.address.country_area,
            },
            "address_source": "shipping",
        },
        line_items=line_items,
        shipping_cost={"amount": shipping_cost},
        expand=["line_items"],
    )

    return prepare_saleor_response_data(resp_data, result)
