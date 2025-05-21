from decimal import Decimal

import pytest

from graphql_client import Money
from nimara_stripe.services.stripe.currencies import (
    get_decimals_for_stripe,
    get_saleor_amount_from_stripe_amount,
    get_stripe_amount_from_saleor_money,
    stripe_currencies,
)

pytestmark = pytest.mark.anyio


async def test_get_decimals_for_stripe_default():
    # Given
    currency = "USD"

    # When
    stripe_decimals = get_decimals_for_stripe(currency=currency)

    # Then
    assert stripe_decimals == 2


async def test_get_decimals_for_stripe():
    # Given
    currency = "BHD"

    # When
    stripe_decimals = get_decimals_for_stripe(currency=currency)

    # Then
    assert stripe_decimals == 3


async def test_get_decimals_for_stripe_lowercase():
    # Given
    currency = "jpy"  # lowercase

    # When
    stripe_decimals = get_decimals_for_stripe(currency=currency)

    # Then
    assert stripe_decimals == 0


async def test_get_decimals_for_stripe_invalid_length():
    # Given
    currency = "USDD"  # 4 letters instead of 3

    # When, Then
    with pytest.raises(ValueError, match="currency needs to be a 3-letter code"):
        get_decimals_for_stripe(currency=currency)


async def test_get_decimals_for_stripe_empty():
    # Given
    currency = ""

    # When, Then
    with pytest.raises(ValueError, match="currency needs to be a 3-letter code"):
        get_decimals_for_stripe(currency=currency)


@pytest.mark.parametrize(
    "currency, amount, expected_output",
    [
        # Two decimals
        ("CHF", Decimal("944"), 94400),
        ("CHF", Decimal("944.4"), 94440),
        ("CHF", Decimal("944.44"), 94444),
        ("CHF", Decimal("944.99"), 94499),
        # Three decimals
        ("BHD", Decimal("499"), 499000),
        ("BHD", Decimal("499.44"), 499440),
        ("BHD", Decimal("499.444"), 499444),
        ("BHD", Decimal("499.999"), 499999),
        # No decimals
        ("JPY", Decimal("499"), 499),
        ("JPY", Decimal("499.00"), 499),
        # Edge cases
        ("USD", Decimal("0"), 0),
        ("USD", Decimal("0.01"), 1),
        ("USD", Decimal("0.1"), 10),
        ("USD", Decimal("1234567.89"), 123456789),
        # Very large number
        ("USD", Decimal("9999999.99"), 999999999),
        # Very small number
        ("BHD", Decimal("0.001"), 1),
    ],
)
async def test_get_stripe_amount_from_saleor_money(currency, amount, expected_output):
    # Given
    money = Money(currency=currency, amount=amount)

    # When
    stripe_amount = get_stripe_amount_from_saleor_money(money=money)

    # Then
    assert stripe_amount == expected_output


@pytest.mark.parametrize(
    "currency, amount, expected_output",
    [
        # Two decimals
        ("CHF", 94400, "944.00"),
        ("CHF", 94440, "944.40"),
        ("CHF", 94444, "944.44"),
        ("CHF", 94499, "944.99"),
        # Three decimals
        ("BHD", 499000, "499.000"),
        ("BHD", 499440, "499.440"),
        ("BHD", 499444, "499.444"),
        ("BHD", 499999, "499.999"),
        # No decimals
        ("JPY", 499, "499"),
        # Edge cases
        ("USD", 0, "0.00"),
        ("USD", 1, "0.01"),
        ("USD", 10, "0.10"),
        ("USD", 123456789, "1234567.89"),
        # Very large number
        ("USD", 999999999, "9999999.99"),
        # Very small number
        ("BHD", 1, "0.001"),
        # Lowercase currency code
        ("usd", 1234, "12.34"),
    ],
)
async def test_get_saleor_amount_from_stripe_amount(currency, amount, expected_output):
    # Given
    # When
    saleor_amount = get_saleor_amount_from_stripe_amount(amount=amount, currency=currency)

    # Then
    assert saleor_amount == expected_output


async def test_stripe_currencies_mapping():
    # Test that all zero-decimal currencies are properly configured
    zero_decimal_currencies = [
        "BIF",
        "CLP",
        "DJF",
        "GNF",
        "JPY",
        "KMF",
        "KRW",
        "MGA",
        "PYG",
        "RWF",
        "UGX",
        "VND",
        "VUV",
        "XAF",
        "XOF",
        "XPF",
    ]

    for currency in zero_decimal_currencies:
        assert stripe_currencies[currency] == 0

    # Test that all three-decimal currencies are properly configured
    three_decimal_currencies = ["BHD", "JOD", "KWD", "OMR", "TND"]

    for currency in three_decimal_currencies:
        assert stripe_currencies[currency] == 3
