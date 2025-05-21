from collections import defaultdict

from jwt.api_jwk import PyJWKSet
from saleor_sdk.marina.jwks import AbstractJWKSClient, AbstractJWKSProvider


class JWKSProvider(AbstractJWKSProvider):  # type: ignore
    jwks_cache: dict[str, str] = defaultdict()

    def __init__(self, jwks_service: AbstractJWKSClient):
        self.jwks_service = jwks_service

    async def get(self, issuer: str, force_refresh: bool = False) -> PyJWKSet:
        """Get JWKS for specified issuer."""
        if issuer not in self.jwks_cache or force_refresh:
            await self.set(issuer, await self.jwks_service.fetch_jwks())
        return PyJWKSet.from_json(self.jwks_cache[issuer])

    async def set(self, issuer: str, jwks: str) -> None:
        """Store JWKS for an issuer in cache."""
        self.jwks_cache[issuer] = jwks
