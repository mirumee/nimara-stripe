import asyncio
import dataclasses
import json
from functools import partial
from typing import cast

from aws_lambda_powertools.utilities.parameters.exceptions import (
    GetParameterError,
    TransformParameterError,
)
from cachetools import TTLCache
from pydantic import RootModel
from pydantic.dataclasses import dataclass as pydantic_dataclass
from saleor_sdk.marina.config import (
    AbstractSaleorConfigProvider,
    SaleorConfigData,
)
from saleor_sdk.marina.exceptions import InvalidSaleorDomain

from nimara_stripe.settings import settings
from nimara_stripe.utils.aws import secrets_client

# The usage of Pydantic's dataclass decorator is important here as it allows us to
# nest dataclasses easier. It also provides a way to validate the data that is being
# passed to the dataclass. Use RootModel[StripeSaleorConfigData](config).model_dump_json()
# to serialize the dataclass to a JSON string.


@pydantic_dataclass
class StripeConfig:
    stripe_pub_key: str
    stripe_secret_key: str
    stripe_webhook_secret_key: str


@pydantic_dataclass
class StripeSaleorConfigData(SaleorConfigData):  # type: ignore
    stripe_configurations_for_channels: dict[str, StripeConfig] = dataclasses.field(
        default_factory=lambda: {}
    )

    def get_stripe_config_for_channel(self, channel_slug: str) -> StripeConfig | None:
        return self.stripe_configurations_for_channels.get(channel_slug)


class StripeSaleorConfigProvider(AbstractSaleorConfigProvider):  # type: ignore
    _cache: TTLCache[str, dict[str, StripeSaleorConfigData]] = TTLCache(maxsize=1, ttl=60)

    async def create_or_update(
        self, auth_token: str, saleor_domain: str, saleor_app_id: str
    ) -> StripeSaleorConfigData:
        configs = await self.get_all()

        config = configs.get(saleor_domain)
        if config:
            config.auth_token = auth_token
            config.saleor_app_id = saleor_app_id
        else:
            config = StripeSaleorConfigData(
                auth_token=auth_token,
                saleor_domain=saleor_domain,
                saleor_app_id=saleor_app_id,
            )

        configs[saleor_domain] = config

        secrets_client.put_secret_value(
            SecretId=settings.secret_app_config_path,
            SecretString=RootModel[dict[str, StripeSaleorConfigData]](configs).model_dump_json(),
        )

        self._cache.clear()

        return config

    async def get_by_saleor_domain(
        self,
        saleor_domain: str,
    ) -> StripeSaleorConfigData:
        configs = await self.get_all()
        if saleor_domain not in configs:
            raise InvalidSaleorDomain(f"Saleor config for {saleor_domain} not found")
        return configs[saleor_domain]

    async def get_all(self) -> dict[str, StripeSaleorConfigData]:
        if "configs" in self._cache:
            return cast(dict[str, StripeSaleorConfigData], self._cache["configs"])
        try:
            response = secrets_client.get_secret_value(
                SecretId=settings.secret_app_config_path,
            )

            secret_string = response.get("SecretString")
            if not secret_string:
                raise InvalidSaleorDomain("Secret is empty")

            config_data = json.loads(secret_string)

            parsed_configs = {
                domain: StripeSaleorConfigData(**raw_config)
                for domain, raw_config in config_data.items()
            }

            self._cache["configs"] = parsed_configs

            return parsed_configs

        except (
            GetParameterError,
            TransformParameterError,
            ValueError,
        ) as e:
            raise InvalidSaleorDomain("Could not retrieve Saleor config list") from e

    async def update_stripe_config_data_by_channel_slug(
        self, saleor_domain: str, channel_slug: str, stripe_config: StripeConfig
    ) -> StripeSaleorConfigData:
        configs = await self.get_all()

        config = configs.get(saleor_domain)
        if not config:
            raise InvalidSaleorDomain(f"Saleor config for {saleor_domain} not found")

        config.stripe_configurations_for_channels[channel_slug] = stripe_config
        configs[saleor_domain] = config

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(
            None,
            partial(
                secrets_client.put_secret_value,
                SecretId=settings.secret_app_config_path,
                SecretString=RootModel[dict[str, StripeSaleorConfigData]](
                    configs
                ).model_dump_json(),
            ),
        )

        self._cache.clear()

        return config

    async def get_by_saleor_app_id(
        self,
        saleor_app_id: str,
    ) -> StripeSaleorConfigData | None:
        raise NotImplementedError()
