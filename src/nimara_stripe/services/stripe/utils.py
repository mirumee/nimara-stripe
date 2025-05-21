def get_result(action_type: str, stripe_result: str) -> str:
    prefixes = {
        "processing": f"{action_type}_REQUEST",
        "requires_payment_method": f"{action_type}_ACTION_REQUIRED",
        "requires_action": f"{action_type}_ACTION_REQUIRED",
        "requires_confirmation": f"{action_type}_ACTION_REQUIRED",
        "canceled": f"{action_type}_FAILURE",
        "succeeded": f"{action_type}_SUCCESS",
        "requires_capture": "AUTHORIZATION_SUCCESS",
    }
    return prefixes.get(stripe_result, "UNKNOWN")
