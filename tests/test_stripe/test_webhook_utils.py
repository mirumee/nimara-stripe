from unittest.mock import AsyncMock

import pytest

from graphql_client import (
    TransactionActionEnum,
    TransactionEventTypeEnum,
)
from nimara_stripe.services.stripe.webhook_utils import (
    get_available_actions_for_type,
    get_refund_updated_event_type,
    handle_payment_intent_event,
)

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "event_data, expected_type, expected_actions",
    [
        (
            {
                "type": "payment_intent.succeeded",
                "capture_method": "manual",
            },
            TransactionEventTypeEnum.AUTHORIZATION_SUCCESS,
            [],
        ),
        (
            {
                "type": "payment_intent.processing",
                "capture_method": "automatic",
            },
            TransactionEventTypeEnum.CHARGE_REQUEST,
            [],
        ),
        (
            {
                "type": "payment_intent.payment_failed",
                "capture_method": "manual",
            },
            TransactionEventTypeEnum.AUTHORIZATION_FAILURE,
            [],
        ),
        (
            {
                "type": "payment_intent.created",
                "capture_method": "automatic",
            },
            TransactionEventTypeEnum.CHARGE_ACTION_REQUIRED,
            [],
        ),
        (
            {
                "type": "payment_intent.canceled",
                "capture_method": "manual",
            },
            TransactionEventTypeEnum.AUTHORIZATION_FAILURE,
            [],
        ),
        (
            {
                "type": "payment_intent.partially_funded",
                "capture_method": "manual",
            },
            TransactionEventTypeEnum.INFO,
            [],
        ),
        (
            {
                "type": "payment_intent.amount_capturable_updated",
                "capture_method": "manual",
            },
            TransactionEventTypeEnum.AUTHORIZATION_ADJUSTMENT,
            ["CHARGE", "CANCEL"],
        ),
        (
            {
                "type": "payment_intent.requires_action",
                "capture_method": "automatic",
            },
            TransactionEventTypeEnum.CHARGE_ACTION_REQUIRED,
            [],
        ),
        (
            {
                "type": "payment_intent.succeeded",
                "capture_method": "automatic",
            },
            TransactionEventTypeEnum.CHARGE_SUCCESS,
            ["REFUND"],
        ),
        (
            {
                "type": "payment_intent.payment_failed",
                "capture_method": "automatic",
            },
            TransactionEventTypeEnum.CHARGE_FAILURE,
            ["CHARGE", "CANCEL"],
        ),
        (
            {
                "type": "charge.refunded",
                "capture_method": "automatic",
            },
            TransactionEventTypeEnum.REFUND_SUCCESS,
            [],
        ),
        (
            {
                "type": "charge.refund.updated",
                "capture_method": "automatic",
                "status": "succeeded",
            },
            TransactionEventTypeEnum.REFUND_SUCCESS,
            [],
        ),
        (
            {
                "type": "charge.refund.updated",
                "capture_method": "automatic",
                "status": "failed",
            },
            TransactionEventTypeEnum.REFUND_FAILURE,
            [],
        ),
        (
            {
                "type": "unknown.event.type",
                "capture_method": "automatic",
            },
            None,
            [],
        ),
    ],
)
async def test_handle_payment_intent_event(event_data, expected_type, expected_actions):
    """Test handling different payment intent events."""
    # Given
    event = AsyncMock()
    event.type = event_data["type"]

    # Create a dictionary with all the needed properties
    obj_dict = {"capture_method": event_data["capture_method"]}

    # Add status for refund.updated events if needed
    if "status" in event_data:
        obj_dict["status"] = event_data["status"]

    # Assign the mock object
    event.data.object = obj_dict

    # When
    result = await handle_payment_intent_event(event)

    # Then
    assert result["type"] == (expected_type.value if expected_type else None)
    assert result["available_actions"] == expected_actions


@pytest.mark.parametrize(
    "payment_intent_status, expected_event_type",
    [
        ("canceled", TransactionEventTypeEnum.REFUND_FAILURE),
        ("pending", TransactionEventTypeEnum.REFUND_REQUEST),
        ("requires_action", TransactionEventTypeEnum.REFUND_REQUEST),
        ("failed", TransactionEventTypeEnum.REFUND_FAILURE),
        ("succeeded", TransactionEventTypeEnum.REFUND_SUCCESS),
        ("unknown_status", None),
        (None, None),  # Added case
    ],
)
async def test_get_refund_updated_event_type(payment_intent_status, expected_event_type):
    """Test that the correct event type is returned for different refund statuses."""
    # When
    result = get_refund_updated_event_type(payment_intent_status)

    # Then
    assert result == expected_event_type


@pytest.mark.parametrize(
    "event_type_enum, expected_actions",
    [
        (TransactionEventTypeEnum.CHARGE_SUCCESS, [TransactionActionEnum.REFUND.value]),
        (
            TransactionEventTypeEnum.CHARGE_FAILURE,
            [TransactionActionEnum.CHARGE.value, TransactionActionEnum.CANCEL.value],
        ),
        (
            TransactionEventTypeEnum.AUTHORIZATION_ADJUSTMENT,
            [
                TransactionActionEnum.CHARGE.value,
                TransactionActionEnum.CANCEL.value,
            ],
        ),
        (TransactionEventTypeEnum.AUTHORIZATION_SUCCESS, []),
        (TransactionEventTypeEnum.AUTHORIZATION_FAILURE, []),
        (TransactionEventTypeEnum.INFO, []),
        (TransactionEventTypeEnum.CHARGE_REQUEST, []),
        (TransactionEventTypeEnum.CHARGE_ACTION_REQUIRED, []),
        (None, []),
    ],
)
async def test_get_available_actions_for_type(event_type_enum, expected_actions):
    """Test that the correct available actions are returned for different event types."""
    # Given, When
    result = get_available_actions_for_type(event_type_enum)

    # Then
    assert result == expected_actions
