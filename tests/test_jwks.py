from unittest.mock import AsyncMock

import pytest
from jwt.api_jwk import PyJWKSet
from saleor_sdk.marina.jwks import AbstractJWKSClient

from nimara_stripe.jwks import JWKSProvider

pytestmark = pytest.mark.anyio


async def test_jwks_provider_set(example_jwks):
    # Given
    mock_client = AsyncMock(spec=AbstractJWKSClient)
    provider = JWKSProvider(mock_client)
    # When
    await provider.set("issuer", example_jwks)
    # Then
    assert provider.jwks_cache == {"issuer": example_jwks}


async def test_jwks_provider_get_from_jwks_service(example_jwks):
    # Given
    mock_client = AsyncMock(spec=AbstractJWKSClient)
    mock_client.fetch_jwks.return_value = example_jwks
    provider = JWKSProvider(mock_client)
    JWKSProvider.jwks_cache = {}  # clear cache
    assert provider.jwks_cache == {}

    # When
    await provider.get("issuer")

    # Then
    mock_client.fetch_jwks.assert_called_once()


async def test_jwks_provider_get_from_jwks_service_force_refresh(example_jwks):
    # Given
    mock_client = AsyncMock(spec=AbstractJWKSClient)
    mock_client.fetch_jwks.return_value = example_jwks
    provider = JWKSProvider(mock_client)

    await provider.set("issuer", example_jwks)

    # When
    await provider.get("issuer", force_refresh=True)

    # Then
    mock_client.fetch_jwks.assert_called_once()


async def test_jwks_provider_get_from_cache(example_jwks):
    # Given
    mock_client = AsyncMock(spec=AbstractJWKSClient)
    mock_client.fetch_jwks.return_value = example_jwks
    provider = JWKSProvider(mock_client)

    await provider.set("issuer", example_jwks)

    # When
    result = await provider.get("issuer")

    # Then
    mock_client.fetch_jwks.assert_not_called()
    assert isinstance(result, PyJWKSet)
