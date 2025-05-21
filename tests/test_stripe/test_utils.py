import pytest

from nimara_stripe.services.stripe.utils import get_result

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "stripe_result,expected",
    [
        ("processing", "TEST_REQUEST"),
        ("requires_payment_method", "TEST_ACTION_REQUIRED"),
        ("requires_action", "TEST_ACTION_REQUIRED"),
        ("requires_confirmation", "TEST_ACTION_REQUIRED"),
        ("canceled", "TEST_FAILURE"),
        ("succeeded", "TEST_SUCCESS"),
        ("requires_capture", "AUTHORIZATION_SUCCESS"),
        ("unknown", "UNKNOWN"),
    ],
)
async def test_get_result(stripe_result, expected):
    # Given, When
    result = get_result(action_type="TEST", stripe_result=stripe_result)
    # Then
    assert result == expected
