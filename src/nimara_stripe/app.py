import asyncio
from typing import Any

from aws_lambda_powertools import Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from fastapi import FastAPI
from lynara import (
    APIGatewayProxyEventV1Interface,
    APIGatewayProxyEventV2Interface,
    Lynara,
)

from nimara_stripe.api.saleor.endpoints import router as saleor_router
from nimara_stripe.api.stripe.endpoints import router as stripe_router
from nimara_stripe.settings import settings
from nimara_stripe.utils.helpers import get_logger

LOGGER = get_logger()
TRACER = Tracer(service=settings.release)

app = FastAPI(
    root_path="/nimara-stripe" if settings.debug else "",
)
app.include_router(stripe_router, prefix="/payment")
app.include_router(saleor_router, prefix="/saleor")

lynara = Lynara(app=app)


@LOGGER.inject_lambda_context(log_event=True)
@TRACER.capture_lambda_handler
def http_handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    api_gw_interface: type[APIGatewayProxyEventV1Interface] | type[APIGatewayProxyEventV2Interface]
    if settings.api_gw_version == 1:
        api_gw_interface = APIGatewayProxyEventV1Interface
    else:
        api_gw_interface = APIGatewayProxyEventV2Interface

    return asyncio.run(lynara.run(event, context, api_gw_interface, base_path=settings.base_path))
