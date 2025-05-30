#!/usr/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "boto3",
#   "boto3_type_annotations",
#   "click",
#   "rich",
# ]
# ///

"""
AWS Local Setup Tool

This script helps set up local AWS resources in Localstack for development purposes.
"""

import sys

import boto3
import click
from boto3_type_annotations.secretsmanager import Client as SecretsClient
from rich.console import Console

console = Console()

DEFAULT_REGION = "eu-central-1"
DEFAULT_ENDPOINT_PORT = 4566


@click.group(chain=True)
@click.option(
    "--localstack-host",
    default="localhost",
    help="Hostname of the Localstack instance",
)
@click.option(
    "--port",
    default=DEFAULT_ENDPOINT_PORT,
    help=f"Port of the Localstack instance (default: {DEFAULT_ENDPOINT_PORT})",
)
@click.option(
    "--region",
    default=DEFAULT_REGION,
    help=f"AWS region to use (default: {DEFAULT_REGION})",
)
@click.pass_context
def cli(ctx: click.Context, localstack_host: str, port: int, region: str) -> None:
    """Set up AWS resources locally in Localstack for development."""
    ctx.ensure_object(dict)
    ctx.obj["localstack_host"] = localstack_host
    ctx.obj["aws_config"] = {
        "region_name": region,
        "endpoint_url": f"http://{localstack_host}:{port}",
        "aws_access_key_id": "000000000000",
        "aws_secret_access_key": "test",
    }
    try:
        ctx.obj["secrets_client"] = boto3.client(
            "secretsmanager", **ctx.obj["aws_config"]
        )
    except Exception as e:
        console.print(f"[bold red]Error connecting to Localstack:[/] {str(e)}")
        console.print(
            f"Make sure Localstack is running at {localstack_host}:{port} or adjust parameters."
        )
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.option(
    "--initial-value",
    default="{}",
    help="Initial value for the secret (default: empty JSON object)",
)
@click.pass_context
def create_secret(ctx: click.Context, name: str, initial_value: str) -> None:
    """Create a new secret in AWS Secrets Manager if it doesn't exist."""
    secrets_client: SecretsClient = ctx.obj["secrets_client"]

    try:
        result = secrets_client.list_secrets(
            Filters=[{"Key": "name", "Values": [name]}]
        )

        if result["SecretList"]:
            console.print(f"Secret '{name}' already exists", style="yellow")
            return

        secrets_client.create_secret(
            Name=name,
            SecretString=initial_value,
        )
        console.print(f"Secret '{name}' created successfully", style="green")
    except Exception as e:
        console.print(f"[bold red]Error creating secret '{name}':[/] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
