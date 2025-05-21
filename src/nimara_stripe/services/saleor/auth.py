from dataclasses import dataclass
from typing import Annotated
from urllib.parse import urlsplit, urlunsplit

from fastapi import Depends, Header, Request
from jwt import decode as jwt_decode
from saleor_sdk.marina.auth import decode_saleor_jwt, verify_webhook_signature
from saleor_sdk.marina.exceptions import Unauthorized

from nimara_stripe.jwks import JWKSProvider
from nimara_stripe.services.saleor.client import SaleorClient
from nimara_stripe.services.saleor.deps import (
    get_saleor_client_class,
    get_saleor_jwks_provider_class,
)
from nimara_stripe.services.saleor.utils import get_saleor_url_parts
from nimara_stripe.utils.helpers import get_logger

LOGGER = get_logger()


@dataclass
class SaleorUser:
    email: str
    iss: str
    user_id: str
    token: str
    is_staff: bool = False
    permissions: list[str] | None = None  # actual permissions of the user in the scope of the app
    user_permissions: list[str] | None = None  # permissions the user have outside of the app

    @property
    def domain(self) -> str:
        return urlsplit(self.iss).netloc

    @property
    def saleor_url(self) -> str:
        parts = urlsplit(self.iss)
        parts = parts._replace(path="")
        return urlunsplit(parts)


async def get_saleor_domain(
    saleor_domain: str = Header(..., alias="Saleor-Domain"),
) -> str:
    return saleor_domain


async def get_saleor_api_url(
    saleor_api_url: str = Header(..., alias="Saleor-Api-Url"),
) -> str:
    return saleor_api_url


async def get_saleor_signature(
    saleor_signature: str = Header(..., alias="Saleor-Signature"),
) -> str:
    return saleor_signature


async def get_saleor_event(saleor_event: str = Header(..., alias="Saleor-Event")) -> str:
    return saleor_event


async def authenticate(saleor_client: SaleorClient, jwt: str) -> SaleorUser:
    user_data = await decode_saleor_jwt(
        jwt=jwt,
        jwks_provider=JWKSProvider(jwks_service=saleor_client),
    )

    return SaleorUser(
        email=user_data["email"],
        is_staff=user_data["is_staff"],
        iss=user_data["iss"],
        token=user_data["token"],
        permissions=user_data.get("permissions"),
        user_permissions=user_data.get("user_permissions"),
        user_id=user_data["user_id"],
    )


async def verify_saleor_webhook(
    request: Request,
    saleor_signature: Annotated[str, Depends(get_saleor_signature)],
    saleor_api_url: Annotated[str, Depends(get_saleor_api_url)],
    saleor_client_class: Annotated[type[SaleorClient], Depends(get_saleor_client_class)],
    jwks_provider_class: Annotated[type[JWKSProvider], Depends(get_saleor_jwks_provider_class)],
) -> None:
    async with saleor_client_class(
        saleor_url=get_saleor_url_parts(saleor_api_url).url, api_key=None
    ) as saleor_client:
        jwks_provider = jwks_provider_class(saleor_client)
        await verify_webhook_signature(
            payload=await request.body(),
            jws=saleor_signature,
            issuer=saleor_api_url,
            jwks_provider=jwks_provider,
            force_refresh=False,
        )


async def saleor_authenticate(
    saleor_domain: str,
    jwt: str,
    saleor_client_class: type[SaleorClient],
) -> SaleorUser:
    unverified_payload = jwt_decode(jwt=jwt, options={"verify_signature": False})
    jwt_saleor_url_parts = get_saleor_url_parts(unverified_payload["iss"])

    if saleor_domain != jwt_saleor_url_parts.domain:
        raise Unauthorized()

    async with saleor_client_class(jwt_saleor_url_parts.url, api_key=None) as saleor:
        try:
            user = await authenticate(saleor_client=saleor, jwt=jwt)
        except Unauthorized:
            raise

        if not user.is_staff:
            raise Unauthorized()

    return user
