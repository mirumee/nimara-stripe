from typing import Annotated

from fastapi import Depends, Form, HTTPException, Query, status
from saleor_sdk.marina.exceptions import Unauthorized

from nimara_stripe.services.saleor.auth import SaleorUser, saleor_authenticate
from nimara_stripe.services.saleor.client import SaleorClient
from nimara_stripe.services.saleor.deps import get_saleor_client_class


async def saleor_authenticate_form(
    saleor_client_class: Annotated[SaleorClient, Depends(get_saleor_client_class)],
    jwt: Annotated[str, Form()],
    saleor_domain: str = Query(..., alias="domain"),
) -> SaleorUser:
    try:
        return await saleor_authenticate(
            saleor_domain=saleor_domain,
            jwt=jwt,
            saleor_client_class=saleor_client_class,
        )
    except Unauthorized as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Saleor token",
        ) from err
