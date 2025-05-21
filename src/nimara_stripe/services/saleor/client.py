import httpx
from saleor_sdk.marina.client import AbstractSaleorClient
from saleor_sdk.marina.exceptions import SaleorAppInstallationProblem
from saleor_sdk.marina.jwks import AbstractJWKSClient

from graphql_client.client import AutoGenClient
from graphql_client.exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidMessageFormat,
    GraphQLClientInvalidResponseError,
)
from nimara_stripe.utils.helpers import get_logger

LOGGER = get_logger()


class SaleorClient(AutoGenClient, AbstractSaleorClient, AbstractJWKSClient):  # type: ignore
    GraphQLClientHttpError = GraphQLClientHttpError
    GraphQlClientInvalidResponseError = GraphQLClientInvalidResponseError
    GraphQLClientGraphQLError = GraphQLClientGraphQLError
    GraphQLClientGraphQLMultiError = GraphQLClientGraphQLMultiError
    GraphQLClientInvalidMessageFormat = GraphQLClientInvalidMessageFormat

    def __init__(
        self,
        saleor_url: str,
        api_key: str | None,
        timeout: httpx.Timeout | None = None,
    ) -> None:
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        if timeout is None:
            timeout = httpx.Timeout(10)
        client = httpx.AsyncClient(
            base_url=saleor_url,
            headers=headers,
            timeout=timeout,
        )
        super().__init__(url="/graphql/", http_client=client)

    async def fetch_jwks(self) -> str:
        response = await self.http_client.get("/.well-known/jwks.json")
        response.raise_for_status()
        return response.content.decode()

    async def get_app_id(self, auth_token: str) -> str | None:
        try:
            app = await self.check_app_token(headers={"Authorization": f"Bearer {auth_token}"})
            if app is None:
                return None
            return app.id
        except GraphQLClientError as err:
            LOGGER.error(str(err))
            raise SaleorAppInstallationProblem(str(err)) from err
