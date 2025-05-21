from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.templating import Jinja2Templates
from saleor_sdk.marina.install import install_app
from saleor_sdk.schemas.manifest import Manifest

from graphql_client import (
    CALCULATE_TAXES_GQL,
    PAYMENT_GATEWAY_INITIALIZE_SESSION_GQL,
    TRANSACTION_CANCELATION_REQUESTED_GQL,
    TRANSACTION_CHARGE_REQUESTED_GQL,
    TRANSACTION_INITIALIZE_SESSION_GQL,
    TRANSACTION_PROCESS_SESSION_GQL,
    TRANSACTION_REFUND_REQUESTED_GQL,
)
from nimara_stripe.api.saleor.deps import saleor_authenticate_form
from nimara_stripe.api.saleor.schema import AppInstallBody
from nimara_stripe.api.saleor.utils import (
    build_url,
    get_config_as_context_data,
    is_allowed_domain,
)
from nimara_stripe.jwks import JWKSProvider
from nimara_stripe.services.saleor.auth import SaleorUser
from nimara_stripe.services.saleor.client import SaleorClient
from nimara_stripe.services.saleor.config import (
    StripeConfig,
    StripeSaleorConfigProvider,
)
from nimara_stripe.services.saleor.deps import (
    SaleorDeps,
    get_saleor_client_class,
    get_saleor_config_provider_class,
    get_saleor_jwks_provider_class,
)
from nimara_stripe.services.saleor.utils import get_saleor_url_parts
from nimara_stripe.settings import SALEOR_APP_ID, settings
from nimara_stripe.utils.helpers import get_logger

if TYPE_CHECKING:
    from starlette.templating import _TemplateResponse


LOGGER = get_logger()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

router = APIRouter()


@router.get("/manifest", name="saleor-manifest")
async def manifest_handler(request: Request) -> Manifest:
    LOGGER.info(request.headers)
    request_host = request.headers.get("host", "")
    body = Manifest.model_validate(
        {
            "id": SALEOR_APP_ID,
            "permissions": ["HANDLE_PAYMENTS", "HANDLE_TAXES"],
            "name": SALEOR_APP_ID,
            "version": "1",
            "about": "Example Nimara Stripe Saleor App ",
            "extensions": [],
            "dataPrivacyUrl": "https://mirumee.com/",
            "homepageUrl": "https://mirumee.com/",
            "supportUrl": "https://mirumee.com/",
            "appUrl": build_url(request_host, "/saleor/app"),
            "tokenTargetUrl": build_url(request_host, "/saleor/register"),
            "webhooks": [
                {
                    "query": PAYMENT_GATEWAY_INITIALIZE_SESSION_GQL,
                    "name": "PaymentGatewayInitializeSession",
                    "targetUrl": build_url(request_host, "/payment/gateway"),
                    "isActive": True,
                    "syncEvents": ["PAYMENT_GATEWAY_INITIALIZE_SESSION"],
                },
                {
                    "query": TRANSACTION_INITIALIZE_SESSION_GQL,
                    "name": "TransactionInitializeSession",
                    "targetUrl": build_url(request_host, "/payment/initialize-session"),
                    "isActive": True,
                    "syncEvents": ["TRANSACTION_INITIALIZE_SESSION"],
                },
                {
                    "query": TRANSACTION_PROCESS_SESSION_GQL,
                    "name": "TransactionProcessSession",
                    "targetUrl": build_url(request_host, "/payment/process-session"),
                    "isActive": True,
                    "syncEvents": ["TRANSACTION_PROCESS_SESSION"],
                },
                {
                    "query": TRANSACTION_CANCELATION_REQUESTED_GQL,
                    "name": "TransactionCancelationRequested",
                    "targetUrl": build_url(request_host, "/payment/cancel"),
                    "isActive": True,
                    "syncEvents": ["TRANSACTION_CANCELATION_REQUESTED"],
                },
                {
                    "query": TRANSACTION_CHARGE_REQUESTED_GQL,
                    "name": "TransactionChargeRequested",
                    "targetUrl": build_url(request_host, "/payment/charge"),
                    "isActive": True,
                    "syncEvents": ["TRANSACTION_CHARGE_REQUESTED"],
                },
                {
                    "query": TRANSACTION_REFUND_REQUESTED_GQL,
                    "name": "TransactionRefundRequested",
                    "targetUrl": build_url(request_host, "/payment/refund"),
                    "isActive": True,
                    "syncEvents": ["TRANSACTION_REFUND_REQUESTED"],
                },
                {
                    "query": CALCULATE_TAXES_GQL,
                    "name": "CalculateTaxes",
                    "targetUrl": build_url(request_host, "/payment/calculate-tax"),
                    "isActive": True,
                    "syncEvents": ["ORDER_CALCULATE_TAXES", "CHECKOUT_CALCULATE_TAXES"],
                },
            ],
        }
    )

    return body


@router.post("/register", name="saleor-register")
async def register_handler(
    register_body: AppInstallBody,
    request: Request,
    saleor_config_provider_class: Annotated[
        type[StripeSaleorConfigProvider], Depends(get_saleor_config_provider_class)
    ],
    saleor_client_class: Annotated[type[SaleorClient], Depends(get_saleor_client_class)],
    jwks_provider_class: Annotated[type[JWKSProvider], Depends(get_saleor_jwks_provider_class)],
) -> str:
    headers = request.headers

    # Extract Saleor domain and API URL from headers
    saleor_domain = headers.get("x-saleor-domain") or headers.get("saleor-domain")
    saleor_url = headers.get("saleor-api-url")

    if not saleor_domain or not saleor_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Saleor domain or API URL in headers.",
        )

    if not is_allowed_domain(saleor_domain, settings.allowed_domain_pattern):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This Saleor domain is not allowed to register the app.",
        )

    config_provider = saleor_config_provider_class()

    LOGGER.info("Register endpoint called", extra={"saleor_domain": saleor_domain})

    async with saleor_client_class(
        saleor_url=get_saleor_url_parts(saleor_url).url,
        api_key=register_body.auth_token,
    ) as saleor_client:
        jwks_provider = jwks_provider_class(jwks_service=saleor_client)

        try:
            LOGGER.info(
                "Starting app installation",
                extra={"auth_token": register_body.auth_token},
            )
            await install_app(
                config_provider=config_provider,
                jwks_provider=jwks_provider,
                saleor_client=saleor_client,
                saleor_domain=saleor_domain,
                saleor_url=saleor_url,
                saleor_auth_token=register_body.auth_token,
            )
            LOGGER.info("App installed successfully")
        except Exception as e:
            LOGGER.exception("Installation failed", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Installation issue."
            )
        return "success!"


@router.get("/app", name="saleor-app")
async def saleor_app(
    request: Request,
    domain: str = Query(..., alias="domain"),
    saleor_api_url: str = Query(..., alias="saleorApiUrl"),
) -> "_TemplateResponse":
    LOGGER.info(
        "App loading page requested",
        extra={"domain": domain, "saleor_api_url": saleor_api_url},
    )
    return templates.TemplateResponse(
        request=request,
        name="loading.html",
        context={
            "request": request,
            "query_params": {
                "domain": domain,
                "saleorApiUrl": saleor_api_url,
            },
        },
    )


@router.post("/app/data/fetch", name="saleor-data-fetch")
async def saleor_data_fetch(
    request: Request,
    saleor_deps: Annotated[SaleorDeps, Depends(SaleorDeps)],
    user: Annotated[SaleorUser, Depends(saleor_authenticate_form)],
) -> "_TemplateResponse":
    LOGGER.info("Data fetch requested", extra={"user_domain": user.domain})
    config_provider = saleor_deps.config_provider_class()
    config = await config_provider.get_by_saleor_domain(
        saleor_domain=user.domain,
    )
    LOGGER.info("Config fetched for domain", extra={"user_domain": user.domain})
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "user": user,
            **get_config_as_context_data(config),
        },
    )


@router.post("/app/data/update-channel-config", name="saleor-data-update-channel-config")
async def saleor_data_update_channel_config(
    request: Request,
    saleor_deps: Annotated[SaleorDeps, Depends(SaleorDeps)],
    user: Annotated[SaleorUser, Depends(saleor_authenticate_form)],
    channel_slug: Annotated[str, Form()],
    stripe_pub_key: Annotated[str, Form()],
    stripe_secret_key: Annotated[str, Form()],
    stripe_webhook_secret_key: Annotated[str, Form()],
) -> "_TemplateResponse":
    LOGGER.info(
        "Updating channel config",
        extra={
            "user_domain": user.domain,
            "channel_slug": channel_slug,
        },
    )
    config_provider = saleor_deps.config_provider_class()
    config = await config_provider.update_stripe_config_data_by_channel_slug(
        user.domain,
        channel_slug,
        StripeConfig(
            stripe_pub_key=stripe_pub_key,
            stripe_secret_key=stripe_secret_key,
            stripe_webhook_secret_key=stripe_webhook_secret_key,
        ),
    )
    LOGGER.info("Channel config updated successfully", extra={"channel_slug": channel_slug})
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "user": user,
            **get_config_as_context_data(config),
        },
    )
