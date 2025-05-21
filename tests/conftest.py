import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm

from nimara_stripe.services.saleor.config import (
    StripeSaleorConfigData,
    StripeSaleorConfigProvider,
)
from nimara_stripe.settings import PROJECT_DIR


@pytest.fixture
def anyio_backend() -> tuple[str, dict[str, bool]]:
    return "asyncio", {"use_uvloop": True}


@pytest.fixture(scope="session")
def rsa_private() -> rsa.RSAPrivateKey:
    with open(Path(__file__).parent.absolute() / "test-snakeoil-rsa-priv", "rb") as rsa_file:
        return cast(
            rsa.RSAPrivateKey,
            serialization.load_pem_private_key(rsa_file.read(), password=None),
        )


@pytest.fixture(scope="session")
def rsa_public(rsa_private) -> rsa.RSAPublicKey:
    return rsa_private.public_key()


def example_jwks_generator(kid: str, rsa_public) -> str:
    jwk_dict = json.loads(RSAAlgorithm.to_jwk(rsa_public))
    jwk_dict.update({"use": "sig", "kid": kid})
    return json.dumps({"keys": [jwk_dict]})


@pytest.fixture(scope="session")
def example_jwks(rsa_public):
    return example_jwks_generator(kid="kid", rsa_public=rsa_public)


def load_data_file(fine_name: str):
    with open(PROJECT_DIR / "tests" / "data" / fine_name) as data_file:
        return json.load(data_file)


@pytest.fixture(scope="function")
def api_gateway_v1_event_payload():
    return load_data_file("api_gateway_v1_event.json")


@pytest.fixture(scope="function")
def api_gateway_v2_event_payload():
    return load_data_file("api_gateway_v2_event.json")


@pytest.fixture(scope="function")
def alb_event_payload():
    return load_data_file("alb_event.json")


@pytest.fixture(scope="function")
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:test"
        aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"

    return LambdaContext()


@pytest.fixture(scope="function")
def saleor_config_provider():
    return StripeSaleorConfigProvider()


@pytest.fixture(scope="function")
def saleor_config_data():
    return StripeSaleorConfigData(
        auth_token="fake_token",
        saleor_domain="example.saleor.com",
        saleor_app_id="fake_app_id",
    )
