from decimal import Decimal
from typing import Any

import stripe

from graphql_client import (
    CalculateTaxesEventCalculateTaxes,
)
from nimara_stripe.services.stripe.currencies import (
    get_saleor_amount_from_stripe_amount,
    get_stripe_amount_from_saleor_money,
)
from nimara_stripe.services.stripe.exceptions import (
    CannotCalculateTaxForZeroNetValueError,
)


def calculate_tax_rate(net: Decimal, tax_value: Decimal) -> Decimal:
    if net == 0:
        raise CannotCalculateTaxForZeroNetValueError
    return (tax_value / net) * 100


def prepare_stripe_data(
    event: CalculateTaxesEventCalculateTaxes,
) -> tuple[int, list["stripe.tax.Calculation.CreateParamsLineItem"]]:
    """This function is preparing data for request to Stripe"""
    shipping_cost = 0
    if event.tax_base.shipping_price:
        shipping_cost = get_stripe_amount_from_saleor_money(event.tax_base.shipping_price)
    line_items: list[stripe.tax.Calculation.CreateParamsLineItem] = []
    for line in event.tax_base.lines:
        product_variant = (
            line.source_line.order_product_variant
            if hasattr(line.source_line, "order_product_variant")
            else line.source_line.checkout_product_variant
        )
        if product_variant is None:
            continue

        line_item: stripe.tax.Calculation.CreateParamsLineItem = {
            "amount": get_stripe_amount_from_saleor_money(line.total_price),
            "quantity": line.quantity,
        }
        if product_variant.product.tax_class:
            line_item["tax_code"] = product_variant.product.tax_class.name
        if line.product_sku:
            line_item["reference"] = line.product_sku

        line_items.append(line_item)
    return shipping_cost, line_items


def prepare_saleor_base_response_data(
    event: CalculateTaxesEventCalculateTaxes,
) -> dict[str, Any]:
    """This function is creating empty response to Saleor"""
    basic_lines = []
    for line in event.tax_base.lines:
        basic_lines.append(
            {
                "tax_rate": 0,
                "total_gross_amount": line.total_price.amount,
                "total_net_amount": line.total_price.amount,
            }
        )
    resp_data = {
        "shipping_tax_rate": 0,
        "shipping_price_gross_amount": event.tax_base.shipping_price.amount,
        "shipping_price_net_amount": event.tax_base.shipping_price.amount,
        "lines": basic_lines,
    }
    return resp_data


def prepare_saleor_response_data(
    resp_data: dict[str, Any], result: stripe.tax.Calculation
) -> dict[str, Any]:
    """This function is populating response to Saleor with actual data"""
    if result.shipping_cost:
        saleorized_shipping_amount = get_saleor_amount_from_stripe_amount(
            amount=result.shipping_cost.amount, currency=result.currency
        )
        saleorized_shipping_tax_amount = get_saleor_amount_from_stripe_amount(
            amount=result.shipping_cost.amount_tax, currency=result.currency
        )
        resp_data.update(
            {
                "shipping_tax_rate": str(
                    calculate_tax_rate(
                        Decimal(saleorized_shipping_amount),
                        Decimal(saleorized_shipping_tax_amount),
                    )
                ),
                "shipping_price_gross_amount": str(
                    Decimal(saleorized_shipping_amount) + Decimal(saleorized_shipping_tax_amount)
                ),
                "shipping_price_net_amount": saleorized_shipping_amount,
            }
        )
    if result.line_items:
        tax_lines = []
        for line in result.line_items.data:
            saleorized_amount = get_saleor_amount_from_stripe_amount(
                amount=line.amount, currency=result.currency
            )
            saleorized_tax_amount = get_saleor_amount_from_stripe_amount(
                amount=line.amount_tax, currency=result.currency
            )
            tax_lines.append(
                {
                    "tax_rate": str(
                        calculate_tax_rate(
                            Decimal(saleorized_amount), Decimal(saleorized_tax_amount)
                        )
                    ),
                    "total_gross_amount": str(
                        Decimal(saleorized_amount) + Decimal(saleorized_tax_amount)
                    ),
                    "total_net_amount": saleorized_amount,
                }
            )
        resp_data.update({"lines": tax_lines})
    return resp_data
