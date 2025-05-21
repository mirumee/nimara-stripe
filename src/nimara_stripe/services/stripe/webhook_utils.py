from typing import TYPE_CHECKING, Any

from graphql_client import (
    TransactionActionEnum,
    TransactionEventTypeEnum,
)

if TYPE_CHECKING:
    from stripe import Event


async def handle_payment_intent_event(event: "Event") -> dict[str, Any]:
    payment_intent = event.data.object
    manual_capture = payment_intent.get("capture_method") == "manual"
    event_type_mapping = {
        "payment_intent.succeeded": (
            TransactionEventTypeEnum.AUTHORIZATION_SUCCESS
            if manual_capture
            else TransactionEventTypeEnum.CHARGE_SUCCESS
        ),
        "payment_intent.processing": (
            TransactionEventTypeEnum.AUTHORIZATION_REQUEST
            if manual_capture
            else TransactionEventTypeEnum.CHARGE_REQUEST
        ),
        "payment_intent.payment_failed": (
            TransactionEventTypeEnum.AUTHORIZATION_FAILURE
            if manual_capture
            else TransactionEventTypeEnum.CHARGE_FAILURE
        ),
        "payment_intent.created": (
            TransactionEventTypeEnum.AUTHORIZATION_ACTION_REQUIRED
            if manual_capture
            else TransactionEventTypeEnum.CHARGE_ACTION_REQUIRED
        ),
        "payment_intent.canceled": (
            TransactionEventTypeEnum.AUTHORIZATION_FAILURE
            if manual_capture
            else TransactionEventTypeEnum.CHARGE_FAILURE
        ),
        "payment_intent.partially_funded": TransactionEventTypeEnum.INFO,
        "payment_intent.amount_capturable_updated": (
            TransactionEventTypeEnum.AUTHORIZATION_ADJUSTMENT
        ),
        "payment_intent.requires_action": (
            TransactionEventTypeEnum.AUTHORIZATION_ACTION_REQUIRED
            if manual_capture
            else TransactionEventTypeEnum.CHARGE_ACTION_REQUIRED
        ),
        "charge.refunded": TransactionEventTypeEnum.REFUND_SUCCESS,
        "charge.refund.updated": get_refund_updated_event_type(payment_intent.get("status")),
    }

    event_type = event_type_mapping.get(event.type)
    available_actions = get_available_actions_for_type(event_type)

    return {
        "type": event_type.value if event_type is not None else None,
        "available_actions": available_actions,
    }


def get_refund_updated_event_type(
    status: str | None,
) -> TransactionEventTypeEnum | None:
    if status in ("canceled", "failed"):
        return TransactionEventTypeEnum.REFUND_FAILURE
    elif status in ("pending", "requires_action"):
        return TransactionEventTypeEnum.REFUND_REQUEST
    elif status == "succeeded":
        return TransactionEventTypeEnum.REFUND_SUCCESS
    return None


def get_available_actions_for_type(
    event_type_enum: TransactionEventTypeEnum | None,
) -> list[str]:
    actions_map = {
        TransactionEventTypeEnum.CHARGE_SUCCESS: [TransactionActionEnum.REFUND.value],
        TransactionEventTypeEnum.CHARGE_FAILURE: [
            TransactionActionEnum.CHARGE.value,
            TransactionActionEnum.CANCEL.value,
        ],
        TransactionEventTypeEnum.AUTHORIZATION_ADJUSTMENT: [
            TransactionActionEnum.CHARGE.value,
            TransactionActionEnum.CANCEL.value,
        ],
    }
    if event_type_enum is None:
        return []
    return actions_map.get(event_type_enum, [])
