from decimal import Decimal

from graphql_client import Money


def get_decimals_for_stripe(currency: str) -> int:
    if len(currency) != 3:
        raise ValueError("currency needs to be a 3-letter code")

    stripe_decimals = stripe_currencies.get(currency.upper(), 2)
    return stripe_decimals


def get_stripe_amount_from_saleor_money(money: Money) -> int:
    amount = Decimal(str(money.amount))
    currency = money.currency
    decimals = get_decimals_for_stripe(currency)
    multiplier = 10**decimals
    return int(amount * multiplier)


def get_saleor_amount_from_stripe_amount(amount: int, currency: str) -> str:
    decimals = get_decimals_for_stripe(currency)
    multiplier = Decimal(10) ** decimals
    return str((Decimal(amount) / multiplier).quantize(Decimal(f"0.{'0' * decimals}")))


# https://docs.stripe.com/development-resources/currency-codes
stripe_currencies: dict[str, int] = {
    "BIF": 0,
    "CLP": 0,
    "DJF": 0,
    "GNF": 0,
    "JPY": 0,
    "KMF": 0,
    "KRW": 0,
    "MGA": 0,
    "PYG": 0,
    "RWF": 0,
    "UGX": 0,
    "VND": 0,
    "VUV": 0,
    "XAF": 0,
    "XOF": 0,
    "XPF": 0,
    "BHD": 3,
    "JOD": 3,
    "KWD": 3,
    "OMR": 3,
    "TND": 3,
}
