from decimal import Decimal
from typing import cast

import pytest
import stripe

from nimara_stripe.api.stripe.utils import (
    calculate_tax_rate,
    prepare_saleor_base_response_data,
    prepare_saleor_response_data,
    prepare_stripe_data,
)
from nimara_stripe.services.stripe.exceptions import CannotCalculateTaxForZeroNetValueError
from tests.test_stripe.stripe_mock import (
    FakeTaxCalculation,
    LineItem,
    LineItemsData,
    Money,
)

pytestmark = pytest.mark.anyio


async def test_calculate_tax():
    result = calculate_tax_rate(Decimal("10.00"), Decimal("2.30"))
    assert result == Decimal("23.00")


async def test_calculate_tax_value_error():
    with pytest.raises(CannotCalculateTaxForZeroNetValueError):
        calculate_tax_rate(Decimal("0"), Decimal("2.30"))


async def test_prepare_stripe_data(saleor_test_calculate_tax_event):
    shipping_cost, line_items = prepare_stripe_data(saleor_test_calculate_tax_event)
    assert shipping_cost == 1000
    assert line_items == [{"amount": 100000, "quantity": 1, "reference": "testSku"}]


async def test_prepare_saleor_base_response_data(saleor_test_calculate_tax_event):
    result = prepare_saleor_base_response_data(saleor_test_calculate_tax_event)
    assert result == {
        "shipping_tax_rate": 0,
        "shipping_price_gross_amount": 10.0,
        "shipping_price_net_amount": 10.0,
        "lines": [{"tax_rate": 0, "total_gross_amount": 1000.0, "total_net_amount": 1000.0}],
    }


async def test_prepare_saleor_response_data():
    test_base_resp_data = {
        "shipping_tax_rate": 0,
        "shipping_price_gross_amount": 10.0,
        "shipping_price_net_amount": 10.0,
        "lines": [{"tax_rate": 0, "total_gross_amount": 1000.0, "total_net_amount": 1000.0}],
    }
    result = prepare_saleor_response_data(
        test_base_resp_data,
        cast(
            stripe.tax.Calculation,
            FakeTaxCalculation(
                amount_total=124230,
                shipping_cost=Money(amount=1000, amount_tax=230),
                currency="PLN",
                line_items=LineItemsData(data=[LineItem(amount=100000, amount_tax=23000)]),
            ),
        ),
    )
    assert result == {
        "shipping_tax_rate": "23.00",
        "shipping_price_gross_amount": "12.30",
        "shipping_price_net_amount": "10.00",
        "lines": [
            {
                "tax_rate": "23.00",
                "total_gross_amount": "1230.00",
                "total_net_amount": "1000.00",
            }
        ],
    }
