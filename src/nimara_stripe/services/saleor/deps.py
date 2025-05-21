from nimara_stripe.jwks import JWKSProvider
from nimara_stripe.services.saleor.client import SaleorClient
from nimara_stripe.services.saleor.config import StripeSaleorConfigProvider


def get_saleor_config_provider_class() -> type[StripeSaleorConfigProvider]:
    return StripeSaleorConfigProvider


def get_saleor_client_class() -> type[SaleorClient]:
    return SaleorClient


def get_saleor_jwks_provider_class() -> type[JWKSProvider]:
    return JWKSProvider


class SaleorDeps:
    config_provider_class: type[StripeSaleorConfigProvider]
    client_class: type[SaleorClient]
    jwks_provider_class: type[JWKSProvider]

    def __init__(self) -> None:
        self.config_provider_class = get_saleor_config_provider_class()
        self.client_class = get_saleor_client_class()
        self.jwks_provider_class = get_saleor_jwks_provider_class()
