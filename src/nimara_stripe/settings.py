"""Application settings for Nimara Stripe integration."""

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings
from saleor_sdk.marina.utils import get_saleor_app_identifier

from nimara_stripe import PROJECT_NAME, VERSION

PROJECT_DIR = Path(__file__).parent.parent.absolute()


class AWSSettings(BaseSettings):
    """AWS configuration settings."""

    aws_endpoint_url: str | None = None
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str | None = None
    aws_default_region: str = "eu-central-1"
    secret_app_config_path: str

    @field_validator("aws_endpoint_url", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: str) -> str | None:
        """Convert empty string to None."""
        return None if v == "" else v


class SaleorSettings(BaseSettings):
    """Saleor-specific settings."""

    environment: str = "dev"
    saleor_timeout: float = 10.0

    _DEFAULT_HTTP_PORTS = [
        80,
        443,
    ]  # Pydantic 2 adds the port even if not specified
    # which makes the comparision difficult


class Settings(SaleorSettings, AWSSettings):
    """Main application settings."""

    project_name: str
    version: str
    release: str
    debug: bool = False
    base_path: str | None = None
    api_gw_version: int = 2
    allowed_domain_pattern: str = ".*"


# Create settings instance
# pyright: reportCallIssue=false
settings = Settings(
    project_name=PROJECT_NAME, version=VERSION, release=f"{PROJECT_NAME}@{VERSION}"
)

# Generate Saleor App ID
SALEOR_APP_ID = get_saleor_app_identifier(settings.environment, settings.project_name)
