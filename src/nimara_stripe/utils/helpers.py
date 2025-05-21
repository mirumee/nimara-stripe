from aws_lambda_powertools import Logger

from nimara_stripe.settings import settings

_LOGGER = Logger(service=settings.release)


def get_logger() -> Logger:
    return _LOGGER
