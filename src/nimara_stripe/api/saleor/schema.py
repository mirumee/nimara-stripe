from pydantic import BaseModel, SecretStr


class AppInstallBody(BaseModel):
    auth_token: str


class StripeConfigResponse(BaseModel):
    stripe_pub_key: SecretStr
    stripe_secret_key: SecretStr
    stripe_webhook_secret_key: SecretStr
