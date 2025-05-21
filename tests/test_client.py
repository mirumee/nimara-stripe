import pytest
from saleor_sdk.marina.exceptions import SaleorAppInstallationProblem

from nimara_stripe.services.saleor.client import SaleorClient

pytestmark = pytest.mark.anyio


async def test_saleor_client_initialization():
    client = SaleorClient(saleor_url="http://example.com", api_key="test_api_key")
    assert client.http_client.base_url == "http://example.com"
    assert client.http_client.headers["Authorization"] == "Bearer test_api_key"


async def test_fetch_jwks(httpx_mock):
    httpx_mock.add_response(url="http://example.com/.well-known/jwks.json", json={"jwks": "data"})

    client = SaleorClient(saleor_url="http://example.com", api_key=None)
    jwks = await client.fetch_jwks()

    assert jwks == '{"jwks":"data"}'


async def test_get_app_id_success(httpx_mock):
    mock_data = {"data": {"app": {"id": "app_id"}}}
    httpx_mock.add_response(url="http://example.com/graphql/", json=mock_data)

    client = SaleorClient(saleor_url="http://example.com", api_key=None)
    app_id = await client.get_app_id("test_auth_token")

    assert app_id == "app_id"


async def test_get_app_id_error(httpx_mock):
    httpx_mock.add_response(
        url="http://example.com/graphql/", json={"errors": [{"message": "error message"}]}
    )

    client = SaleorClient(saleor_url="http://example.com", api_key=None)
    with pytest.raises(SaleorAppInstallationProblem):
        await client.get_app_id("test_auth_token")
