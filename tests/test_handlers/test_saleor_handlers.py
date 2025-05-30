import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from saleor_sdk.marina.exceptions import SaleorAppInstallationProblem

from nimara_stripe.api.saleor.app import app

pytestmark = pytest.mark.anyio

client = TestClient(app)


async def test_manifest_handler():
    request_host = "example.com"

    response = client.get("/saleor/manifest", headers={"host": request_host})

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == "DEV.nimara-stripe"
    assert response_data["appUrl"] == f"https://{request_host}/saleor/app"


async def test_register_handler_success(mocker: MockerFixture):
    mock_install = mocker.patch(
        "nimara_stripe.api.saleor.endpoints.install_app",
        new_callable=mocker.AsyncMock,
    )

    response = client.post(
        "/saleor/register",
        json={"auth_token": "valid_token"},
        headers={
            "Saleor-Domain": "example.saleor.com",
            "saleor-api-url": "http://example.saleor.com/graphql/",
        },
    )

    assert response.status_code == 200
    mock_install.assert_called_once()


async def test_register_handler_installation_problem(
    mocker: MockerFixture,
):
    mock_install = mocker.patch(
        "nimara_stripe.api.saleor.endpoints.install_app",
        new_callable=mocker.AsyncMock,
    )
    mock_install.side_effect = SaleorAppInstallationProblem()

    response = client.post(
        "/saleor/register",
        json={"auth_token": "valid_token"},
        headers={
            "Saleor-Domain": "example.saleor.com",
            "saleor-api-url": "http://example.saleor.com/graphql/",
        },
    )

    mock_install.assert_called_once()
    assert response.status_code == 400


async def test_register_handler_no_body(
    mocker: MockerFixture,
):
    mock_install = mocker.patch(
        "nimara_stripe.api.saleor.endpoints.install_app",
        new_callable=mocker.AsyncMock,
    )

    response = client.post(
        "/saleor/register",
        json={"auth_token": "valid_token"},
        headers={
            "Saleor-Domain": "example.saleor.com",
            "saleor-api-url": "http://example.saleor.com/graphql/",
        },
    )

    mock_install.assert_called_once()
    assert response.status_code == 200
