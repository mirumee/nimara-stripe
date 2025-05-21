from dataclasses import dataclass


@dataclass
class Money:
    amount: int
    amount_tax: int


@dataclass
class LineItem:
    amount: int
    amount_tax: int


@dataclass
class LineItemsData:
    data: list[LineItem]


@dataclass
class LastPaymentError:
    status: str | None
    message: str | None


@dataclass
class FakePaymentIntent:
    id: str
    amount: int
    currency: str
    status: str
    client_secret: str
    created: str
    cancellation_reason: str
    description: str
    last_payment_error: LastPaymentError | None


@dataclass
class FakeTaxCalculation:
    amount_total: int
    shipping_cost: Money
    currency: str
    line_items: LineItemsData
