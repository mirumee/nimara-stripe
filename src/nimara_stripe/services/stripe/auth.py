from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, Header, Request

from nimara_stripe.services.saleor.config import StripeConfig

if TYPE_CHECKING:
    from types import ModuleType


async def get_stripe_signature(
    stripe_signature: str = Header(..., alias="stripe-signature"),
) -> str:
    return stripe_signature


async def validate_stripe_webhook(
    request: Request,
    stripe_signature: Annotated[str, Depends(get_stripe_signature)],
    stripe_config: StripeConfig,
    stripe: "ModuleType",
) -> None:
    stripe.Webhook.construct_event(
        payload=await request.body(),
        sig_header=stripe_signature,
        secret=stripe_config.stripe_webhook_secret_key,
    )
