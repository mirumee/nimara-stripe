import boto3
from boto3_type_annotations.secretsmanager import Client as SecretsClient

from nimara_stripe.settings import settings

aws_config = {
    "region_name": settings.aws_default_region,
    "endpoint_url": settings.aws_endpoint_url,
    "aws_access_key_id": settings.aws_access_key_id,
    "aws_secret_access_key": settings.aws_secret_access_key,
    "aws_session_token": settings.aws_session_token,
}

secrets_client: SecretsClient = boto3.client("secretsmanager", **aws_config)
