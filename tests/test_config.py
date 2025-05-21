import json
from unittest.mock import patch

import pytest
from aws_lambda_powertools.utilities.parameters.exceptions import GetParameterError
from pydantic import RootModel
from pytest_mock import MockerFixture
from saleor_sdk.marina.exceptions import InvalidSaleorDomain

from nimara_stripe.services.saleor.config import (
    StripeSaleorConfigData,
    StripeSaleorConfigProvider,
)
from nimara_stripe.settings import settings

pytestmark = pytest.mark.anyio


@patch("nimara_stripe.services.saleor.config.secrets_client")
async def test_create_or_update_no_item_in_secret_manager(
    mock_secrets_client,
    saleor_config_data: StripeSaleorConfigData,
    saleor_config_provider: StripeSaleorConfigProvider,
    mocker: MockerFixture,
):
    # Given
    mock_get_all = mocker.AsyncMock(return_value={})
    mocker.patch.object(
        saleor_config_provider,
        "get_all",
        mock_get_all,
    )

    # When
    result = await saleor_config_provider.create_or_update(
        saleor_config_data.auth_token,
        saleor_config_data.saleor_domain,
        saleor_config_data.saleor_app_id,
    )

    # Then
    assert result == saleor_config_data
    mock_get_all.assert_awaited_once()
    mock_secrets_client.put_secret_value.assert_called_once_with(
        SecretId=settings.secret_app_config_path,
        SecretString=RootModel[dict[str, StripeSaleorConfigData]](
            {saleor_config_data.saleor_domain: saleor_config_data}
        ).model_dump_json(),
    )


@patch("nimara_stripe.services.saleor.config.secrets_client")
async def test_create_or_update_item_in_secret_manager(
    mock_secrets_client,
    saleor_config_data: StripeSaleorConfigData,
    saleor_config_provider: StripeSaleorConfigProvider,
    mocker: MockerFixture,
):
    # Given
    # Mock functions
    mock_get_all = mocker.AsyncMock(
        return_value={saleor_config_data.saleor_domain: saleor_config_data}
    )
    mocker.patch.object(
        saleor_config_provider,
        "get_all",
        mock_get_all,
    )

    # When
    result = await saleor_config_provider.create_or_update(
        saleor_config_data.auth_token,
        saleor_config_data.saleor_domain,
        saleor_config_data.saleor_app_id,
    )

    # Then
    assert result == saleor_config_data
    mock_get_all.assert_awaited_once()
    mock_secrets_client.put_secret_value.assert_called_once_with(
        SecretId=settings.secret_app_config_path,
        SecretString=RootModel[dict[str, StripeSaleorConfigData]](
            {saleor_config_data.saleor_domain: saleor_config_data}
        ).model_dump_json(),
    )


@patch("nimara_stripe.services.saleor.config.secrets_client")
async def test_get_by_saleor_domain_data_in_secret_manager(
    mock_secrets_client,
    saleor_config_data: StripeSaleorConfigData,
    saleor_config_provider: StripeSaleorConfigProvider,
):
    # Given
    domain = saleor_config_data.saleor_domain
    version_id = "mock-version-id"
    serialized_config = RootModel[StripeSaleorConfigData](saleor_config_data).model_dump()

    secret_dict = {domain: serialized_config}
    secret_string = json.dumps(secret_dict)

    mock_secrets_client.get_secret_value.return_value = {
        "SecretString": secret_string,
        "VersionId": version_id,
    }

    # When
    result = await saleor_config_provider.get_by_saleor_domain(
        saleor_config_data.saleor_domain,
    )

    # Then
    assert result == saleor_config_data
    mock_secrets_client.get_secret_value.assert_called_once_with(
        SecretId=settings.secret_app_config_path,
    )


@patch("nimara_stripe.services.saleor.config.secrets_client")
async def test_get_by_saleor_domain_no_data_in_secret_manager(
    mock_secrets_client,
    saleor_config_data: StripeSaleorConfigData,
    saleor_config_provider: StripeSaleorConfigProvider,
):
    # Given
    StripeSaleorConfigProvider._cache.clear()
    mock_secrets_client.get_secret_value.side_effect = GetParameterError()

    # When
    with pytest.raises(InvalidSaleorDomain):
        await saleor_config_provider.get_by_saleor_domain(
            saleor_config_data.saleor_domain,
        )

    # Then
    mock_secrets_client.get_secret_value.assert_called_once_with(
        SecretId=settings.secret_app_config_path,
    )


async def test_get_by_saleor_app_id(saleor_config_provider: StripeSaleorConfigProvider):
    with pytest.raises(NotImplementedError):
        await saleor_config_provider.get_by_saleor_app_id("id")
