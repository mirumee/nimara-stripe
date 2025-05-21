from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from lynara import APIGatewayProxyEventV1Interface, APIGatewayProxyEventV2Interface

from nimara_stripe.app import (
    http_handler,
    settings,
)

pytestmark = pytest.mark.anyio


@patch("nimara_stripe.app.asyncio.run")
@patch("nimara_stripe.app.lynara.run")
def test_http_handler_apigw_v1(mock_lynara_run, mock_asyncio_run):
    # Given
    event = {"version": "1.0"}
    context = MagicMock()

    # Set API Gateway version to 1 for this test
    original_api_gw_version = settings.api_gw_version
    settings.api_gw_version = 1

    mock_asyncio_run.return_value = {"statusCode": 200}
    mock_lynara_run.return_value = {"statusCode": 200}

    # When
    result = http_handler(event, context)

    # Then
    mock_lynara_run.assert_called_once_with(
        event,
        context,
        APIGatewayProxyEventV1Interface,
        base_path=settings.base_path,
    )
    mock_asyncio_run.assert_called_once()
    assert result == {"statusCode": 200}

    # Cleanup
    settings.api_gw_version = original_api_gw_version


@patch("nimara_stripe.app.asyncio.run")
@patch("nimara_stripe.app.lynara.run")
def test_http_handler_apigw_v2(mock_lynara_run, mock_asyncio_run):
    # Given
    event = {"version": "2.0"}
    context = MagicMock()

    # Set API Gateway version to 2 for this test
    original_api_gw_version = settings.api_gw_version
    settings.api_gw_version = 2

    mock_asyncio_run.return_value = {"statusCode": 200}
    mock_lynara_run.return_value = {"statusCode": 200}

    # When
    result = http_handler(event, context)

    # Then
    mock_lynara_run.assert_called_once_with(
        event,
        context,
        APIGatewayProxyEventV2Interface,
        base_path=settings.base_path,
    )
    mock_asyncio_run.assert_called_once()
    assert result == {"statusCode": 200}

    # Cleanup
    settings.api_gw_version = original_api_gw_version


def test_root_path_with_debug_true():
    # Given
    original_debug = settings.debug
    settings.debug = True

    # When
    test_app = FastAPI(
        root_path="/nimara-stripe" if settings.debug else "",
    )

    # Then
    assert test_app.root_path == "/nimara-stripe"

    # Cleanup
    settings.debug = original_debug


def test_root_path_with_debug_false():
    # Given
    original_debug = settings.debug
    settings.debug = False

    # When
    test_app = FastAPI(
        root_path="/nimara-stripe" if settings.debug else "",
    )

    # Then
    assert test_app.root_path == ""

    # Cleanup
    settings.debug = original_debug
