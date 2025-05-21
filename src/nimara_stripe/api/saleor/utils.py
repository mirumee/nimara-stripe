import re

from fastapi import HTTPException, status
from pydantic import SecretStr

from nimara_stripe.api.saleor.schema import StripeConfigResponse
from nimara_stripe.services.saleor.config import StripeSaleorConfigData
from nimara_stripe.settings import settings


def build_url(request_host: str, endpoint: str) -> str:
    if settings.debug:
        return f"https://{request_host}/nimara-stripe{endpoint}"
    return f"https://{request_host}{endpoint}"


def get_config_as_context_data(
    config: StripeSaleorConfigData,
) -> dict[str, str | SecretStr | dict[str, StripeConfigResponse]]:
    return {
        "saleor_domain": config.saleor_domain,
        "saleor_app_id": config.saleor_app_id,
        "auth_token": SecretStr(config.auth_token),
        "config_per_channel": {
            channel_slug: StripeConfigResponse(
                stripe_pub_key=SecretStr(stripe_config.stripe_pub_key),
                stripe_secret_key=SecretStr(stripe_config.stripe_secret_key),
                stripe_webhook_secret_key=SecretStr(stripe_config.stripe_webhook_secret_key),
            )
            for channel_slug, stripe_config in config.stripe_configurations_for_channels.items()
        },
    }


def is_allowed_domain(domain: str, pattern: str) -> bool:
    try:
        return re.search(pattern, domain) is not None
    except re.error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid domain pattern configured on server.",
        )
