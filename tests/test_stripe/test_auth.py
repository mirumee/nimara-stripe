from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import Request
from stripe import StripeError

from nimara_stripe.services.saleor.config import StripeConfig
from nimara_stripe.services.stripe.auth import (
    get_stripe_signature,
    validate_stripe_webhook,
)

pytestmark = pytest.mark.anyio


async def test_get_stripe_signature():
    # Given
    expected_signature = "whsec_test_signature"

    # When
    signature = await get_stripe_signature(stripe_signature=expected_signature)

    # Then
    assert signature == expected_signature


async def test_validate_stripe_webhook_valid_signature():
    # Given
    mock_request = AsyncMock(spec=Request)
    mock_request.body.return_value = b'{"test": "payload"}'

    stripe_signature = "valid_signature"
    stripe_config = StripeConfig(
        stripe_pub_key="pk_test",
        stripe_secret_key="sk_test",
        stripe_webhook_secret_key="whsec_test",
    )

    mock_stripe = MagicMock()
    mock_webhook = MagicMock()
    mock_stripe.Webhook = mock_webhook

    # When
    await validate_stripe_webhook(
        request=mock_request,
        stripe_signature=stripe_signature,
        stripe_config=stripe_config,
        stripe=mock_stripe,
    )

    # Then
    mock_webhook.construct_event.assert_called_once_with(
        payload=b'{"test": "payload"}',
        sig_header=stripe_signature,
        secret=stripe_config.stripe_webhook_secret_key,
    )


async def test_validate_stripe_webhook_invalid_signature():
    # Given
    mock_request = AsyncMock(spec=Request)
    mock_request.body.return_value = b'{"test": "payload"}'

    stripe_signature = "invalid_signature"
    stripe_config = StripeConfig(
        stripe_pub_key="pk_test",
        stripe_secret_key="sk_test",
        stripe_webhook_secret_key="whsec_test",
    )

    mock_stripe = MagicMock()
    mock_webhook = MagicMock()
    mock_stripe.Webhook = mock_webhook

    # Setup the mock to raise an exception
    mock_webhook.construct_event.side_effect = StripeError("Invalid signature", "sig_header")

    # When, Then
    with pytest.raises(StripeError, match="Invalid signature"):
        await validate_stripe_webhook(
            request=mock_request,
            stripe_signature=stripe_signature,
            stripe_config=stripe_config,
            stripe=mock_stripe,
        )

    # Verify the mock was called with the expected arguments
    mock_webhook.construct_event.assert_called_once_with(
        payload=b'{"test": "payload"}',
        sig_header=stripe_signature,
        secret=stripe_config.stripe_webhook_secret_key,
    )
