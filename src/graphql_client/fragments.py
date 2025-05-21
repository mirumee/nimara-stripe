from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import LanguageCodeEnum, TransactionActionEnum, TransactionFlowStrategyEnum


class Address(BaseModel):
    street_address_1: str = Field(alias="streetAddress1")
    street_address_2: str = Field(alias="streetAddress2")
    city: str
    country_area: str = Field(alias="countryArea")
    postal_code: str = Field(alias="postalCode")
    country: "AddressCountry"


class AddressCountry(BaseModel):
    code: str


class Money(BaseModel):
    currency: str
    amount: float


class PaymentGatewayInitializeSessionAddress(BaseModel):
    country: "PaymentGatewayInitializeSessionAddressCountry"


class PaymentGatewayInitializeSessionAddressCountry(BaseModel):
    code: str


class PaymentGatewayRecipient(BaseModel):
    id: str
    private_metadata: List["PaymentGatewayRecipientPrivateMetadata"] = Field(
        alias="privateMetadata"
    )
    metadata: List["PaymentGatewayRecipientMetadata"]


class PaymentGatewayRecipientPrivateMetadata(BaseModel):
    key: str
    value: str


class PaymentGatewayRecipientMetadata(BaseModel):
    key: str
    value: str


class PaymentGatewayInitializeSessionEvent(BaseModel):
    typename__: str = Field(alias="__typename")
    recipient: Optional["PaymentGatewayInitializeSessionEventRecipient"]
    data: Optional[Any]
    amount: Optional[Any]
    issuing_principal: Optional[
        Annotated[
            Union[
                "PaymentGatewayInitializeSessionEventIssuingPrincipalApp",
                "PaymentGatewayInitializeSessionEventIssuingPrincipalUser",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="issuingPrincipal")
    source_object: Union[
        "PaymentGatewayInitializeSessionEventSourceObjectCheckout",
        "PaymentGatewayInitializeSessionEventSourceObjectOrder",
    ] = Field(alias="sourceObject", discriminator="typename__")


class PaymentGatewayInitializeSessionEventRecipient(PaymentGatewayRecipient):
    pass


class PaymentGatewayInitializeSessionEventIssuingPrincipalApp(BaseModel):
    typename__: Literal["App"] = Field(alias="__typename")
    id: str


class PaymentGatewayInitializeSessionEventIssuingPrincipalUser(BaseModel):
    typename__: Literal["User"] = Field(alias="__typename")
    id: str


class PaymentGatewayInitializeSessionEventSourceObjectCheckout(BaseModel):
    typename__: Literal["Checkout"] = Field(alias="__typename")
    id: str
    channel: "PaymentGatewayInitializeSessionEventSourceObjectCheckoutChannel"
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    billing_address: Optional[
        "PaymentGatewayInitializeSessionEventSourceObjectCheckoutBillingAddress"
    ] = Field(alias="billingAddress")
    total: "PaymentGatewayInitializeSessionEventSourceObjectCheckoutTotal"


class PaymentGatewayInitializeSessionEventSourceObjectCheckoutChannel(BaseModel):
    id: str
    slug: str


class PaymentGatewayInitializeSessionEventSourceObjectCheckoutBillingAddress(
    PaymentGatewayInitializeSessionAddress
):
    pass


class PaymentGatewayInitializeSessionEventSourceObjectCheckoutTotal(BaseModel):
    gross: "PaymentGatewayInitializeSessionEventSourceObjectCheckoutTotalGross"


class PaymentGatewayInitializeSessionEventSourceObjectCheckoutTotalGross(Money):
    pass


class PaymentGatewayInitializeSessionEventSourceObjectOrder(BaseModel):
    typename__: Literal["Order"] = Field(alias="__typename")
    id: str
    channel: "PaymentGatewayInitializeSessionEventSourceObjectOrderChannel"
    language_code_enum: LanguageCodeEnum = Field(alias="languageCodeEnum")
    user_email: Optional[str] = Field(alias="userEmail")
    billing_address: Optional[
        "PaymentGatewayInitializeSessionEventSourceObjectOrderBillingAddress"
    ] = Field(alias="billingAddress")
    total: "PaymentGatewayInitializeSessionEventSourceObjectOrderTotal"


class PaymentGatewayInitializeSessionEventSourceObjectOrderChannel(BaseModel):
    id: str
    slug: str


class PaymentGatewayInitializeSessionEventSourceObjectOrderBillingAddress(
    PaymentGatewayInitializeSessionAddress
):
    pass


class PaymentGatewayInitializeSessionEventSourceObjectOrderTotal(BaseModel):
    gross: "PaymentGatewayInitializeSessionEventSourceObjectOrderTotalGross"


class PaymentGatewayInitializeSessionEventSourceObjectOrderTotalGross(Money):
    pass


class TaxBaseLine(BaseModel):
    source_line: Union[
        "TaxBaseLineSourceLineCheckoutLine", "TaxBaseLineSourceLineOrderLine"
    ] = Field(alias="sourceLine", discriminator="typename__")
    quantity: int
    unit_price: "TaxBaseLineUnitPrice" = Field(alias="unitPrice")
    total_price: "TaxBaseLineTotalPrice" = Field(alias="totalPrice")
    product_sku: Optional[str] = Field(alias="productSku")


class TaxBaseLineSourceLineCheckoutLine(BaseModel):
    typename__: Literal["CheckoutLine"] = Field(alias="__typename")
    id: str
    checkout_product_variant: (
        "TaxBaseLineSourceLineCheckoutLineCheckoutProductVariant"
    ) = Field(alias="checkoutProductVariant")


class TaxBaseLineSourceLineCheckoutLineCheckoutProductVariant(BaseModel):
    id: str
    product: "TaxBaseLineSourceLineCheckoutLineCheckoutProductVariantProduct"


class TaxBaseLineSourceLineCheckoutLineCheckoutProductVariantProduct(BaseModel):
    tax_class: Optional[
        "TaxBaseLineSourceLineCheckoutLineCheckoutProductVariantProductTaxClass"
    ] = Field(alias="taxClass")


class TaxBaseLineSourceLineCheckoutLineCheckoutProductVariantProductTaxClass(BaseModel):
    id: str
    name: str


class TaxBaseLineSourceLineOrderLine(BaseModel):
    typename__: Literal["OrderLine"] = Field(alias="__typename")
    id: str
    order_product_variant: Optional[
        "TaxBaseLineSourceLineOrderLineOrderProductVariant"
    ] = Field(alias="orderProductVariant")


class TaxBaseLineSourceLineOrderLineOrderProductVariant(BaseModel):
    id: str
    product: "TaxBaseLineSourceLineOrderLineOrderProductVariantProduct"


class TaxBaseLineSourceLineOrderLineOrderProductVariantProduct(BaseModel):
    tax_class: Optional[
        "TaxBaseLineSourceLineOrderLineOrderProductVariantProductTaxClass"
    ] = Field(alias="taxClass")


class TaxBaseLineSourceLineOrderLineOrderProductVariantProductTaxClass(BaseModel):
    id: str
    name: str


class TaxBaseLineUnitPrice(BaseModel):
    amount: float


class TaxBaseLineTotalPrice(Money):
    pass


class TaxDiscount(BaseModel):
    name: Optional[str]
    amount: "TaxDiscountAmount"


class TaxDiscountAmount(BaseModel):
    amount: float


class TaxBase(BaseModel):
    prices_entered_with_tax: bool = Field(alias="pricesEnteredWithTax")
    currency: str
    channel: "TaxBaseChannel"
    discounts: List["TaxBaseDiscounts"]
    address: Optional["TaxBaseAddress"]
    shipping_price: "TaxBaseShippingPrice" = Field(alias="shippingPrice")
    lines: List["TaxBaseLines"]


class TaxBaseChannel(BaseModel):
    slug: str


class TaxBaseDiscounts(TaxDiscount):
    pass


class TaxBaseAddress(Address):
    pass


class TaxBaseShippingPrice(Money):
    pass


class TaxBaseLines(TaxBaseLine):
    pass


class TransactionCancelationRequestedEvent(BaseModel):
    typename__: str = Field(alias="__typename")
    recipient: Optional["TransactionCancelationRequestedEventRecipient"]
    action: "TransactionCancelationRequestedEventAction"
    transaction: Optional["TransactionCancelationRequestedEventTransaction"]


class TransactionCancelationRequestedEventRecipient(PaymentGatewayRecipient):
    pass


class TransactionCancelationRequestedEventAction(BaseModel):
    action_type: TransactionActionEnum = Field(alias="actionType")
    currency: str
    amount: Optional[Any]


class TransactionCancelationRequestedEventTransaction(BaseModel):
    id: str
    psp_reference: str = Field(alias="pspReference")
    source_object: Optional[
        "TransactionCancelationRequestedEventTransactionSourceObject"
    ] = Field(alias="sourceObject")


class TransactionCancelationRequestedEventTransactionSourceObject(BaseModel):
    channel: "TransactionCancelationRequestedEventTransactionSourceObjectChannel"


class TransactionCancelationRequestedEventTransactionSourceObjectChannel(BaseModel):
    id: str
    slug: str


class TransactionChargeRequestedEvent(BaseModel):
    typename__: str = Field(alias="__typename")
    recipient: Optional["TransactionChargeRequestedEventRecipient"]
    action: "TransactionChargeRequestedEventAction"
    transaction: Optional["TransactionChargeRequestedEventTransaction"]


class TransactionChargeRequestedEventRecipient(PaymentGatewayRecipient):
    pass


class TransactionChargeRequestedEventAction(BaseModel):
    amount: Optional[Any]
    currency: str
    action_type: TransactionActionEnum = Field(alias="actionType")


class TransactionChargeRequestedEventTransaction(BaseModel):
    id: str
    psp_reference: str = Field(alias="pspReference")
    source_object: Optional[
        "TransactionChargeRequestedEventTransactionSourceObject"
    ] = Field(alias="sourceObject")


class TransactionChargeRequestedEventTransactionSourceObject(BaseModel):
    total: "TransactionChargeRequestedEventTransactionSourceObjectTotal"
    typename__: Literal["Order"] = Field(alias="__typename")
    channel: "TransactionChargeRequestedEventTransactionSourceObjectChannel"
    shipping_price: (
        "TransactionChargeRequestedEventTransactionSourceObjectShippingPrice"
    ) = Field(alias="shippingPrice")
    delivery_method: Optional[
        Annotated[
            Union[
                "TransactionChargeRequestedEventTransactionSourceObjectDeliveryMethodWarehouse",
                "TransactionChargeRequestedEventTransactionSourceObjectDeliveryMethodShippingMethod",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="deliveryMethod")
    lines: List["TransactionChargeRequestedEventTransactionSourceObjectLines"]


class TransactionChargeRequestedEventTransactionSourceObjectTotal(BaseModel):
    gross: "TransactionChargeRequestedEventTransactionSourceObjectTotalGross"


class TransactionChargeRequestedEventTransactionSourceObjectTotalGross(Money):
    pass


class TransactionChargeRequestedEventTransactionSourceObjectChannel(BaseModel):
    id: str
    slug: str


class TransactionChargeRequestedEventTransactionSourceObjectShippingPrice(BaseModel):
    gross: "TransactionChargeRequestedEventTransactionSourceObjectShippingPriceGross"
    net: "TransactionChargeRequestedEventTransactionSourceObjectShippingPriceNet"
    tax: "TransactionChargeRequestedEventTransactionSourceObjectShippingPriceTax"


class TransactionChargeRequestedEventTransactionSourceObjectShippingPriceGross(Money):
    pass


class TransactionChargeRequestedEventTransactionSourceObjectShippingPriceNet(Money):
    pass


class TransactionChargeRequestedEventTransactionSourceObjectShippingPriceTax(Money):
    pass


class TransactionChargeRequestedEventTransactionSourceObjectDeliveryMethodWarehouse(
    BaseModel
):
    typename__: Literal["Warehouse"] = Field(alias="__typename")


class TransactionChargeRequestedEventTransactionSourceObjectDeliveryMethodShippingMethod(
    BaseModel
):
    typename__: Literal["ShippingMethod"] = Field(alias="__typename")
    id: str
    name: str


class TransactionChargeRequestedEventTransactionSourceObjectLines(BaseModel):
    typename__: Literal["OrderLine"] = Field(alias="__typename")
    id: str
    quantity: int
    tax_rate: float = Field(alias="taxRate")
    total_price: (
        "TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPrice"
    ) = Field(alias="totalPrice")
    order_variant: Optional[
        "TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariant"
    ] = Field(alias="orderVariant")


class TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPrice(BaseModel):
    gross: "TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceGross"
    net: "TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceNet"
    tax: "TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceTax"


class TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceGross(Money):
    pass


class TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceNet(Money):
    pass


class TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceTax(Money):
    pass


class TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariant(
    BaseModel
):
    name: str
    sku: Optional[str]
    product: (
        "TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProduct"
    )


class TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProduct(
    BaseModel
):
    name: str
    thumbnail: Optional[
        "TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProductThumbnail"
    ]
    category: Optional[
        "TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProductCategory"
    ]


class TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProductThumbnail(
    BaseModel
):
    url: str


class TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProductCategory(
    BaseModel
):
    name: str


class TransactionInitializeSessionAddress(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    phone: Optional[str]
    city: str
    street_address_1: str = Field(alias="streetAddress1")
    street_address_2: str = Field(alias="streetAddress2")
    postal_code: str = Field(alias="postalCode")
    country_area: str = Field(alias="countryArea")
    company_name: str = Field(alias="companyName")
    country: "TransactionInitializeSessionAddressCountry"


class TransactionInitializeSessionAddressCountry(BaseModel):
    code: str


class TransactionInitializeSessionEvent(BaseModel):
    typename__: str = Field(alias="__typename")
    recipient: Optional["TransactionInitializeSessionEventRecipient"]
    data: Optional[Any]
    merchant_reference: str = Field(alias="merchantReference")
    action: "TransactionInitializeSessionEventAction"
    issuing_principal: Optional[
        Annotated[
            Union[
                "TransactionInitializeSessionEventIssuingPrincipalApp",
                "TransactionInitializeSessionEventIssuingPrincipalUser",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="issuingPrincipal")
    transaction: "TransactionInitializeSessionEventTransaction"
    source_object: Union[
        "TransactionInitializeSessionEventSourceObjectCheckout",
        "TransactionInitializeSessionEventSourceObjectOrder",
    ] = Field(alias="sourceObject", discriminator="typename__")


class TransactionInitializeSessionEventRecipient(PaymentGatewayRecipient):
    pass


class TransactionInitializeSessionEventAction(BaseModel):
    amount: Any
    currency: str
    action_type: TransactionFlowStrategyEnum = Field(alias="actionType")


class TransactionInitializeSessionEventIssuingPrincipalApp(BaseModel):
    typename__: Literal["App"] = Field(alias="__typename")
    id: str


class TransactionInitializeSessionEventIssuingPrincipalUser(BaseModel):
    typename__: Literal["User"] = Field(alias="__typename")
    id: str


class TransactionInitializeSessionEventTransaction(BaseModel):
    id: str
    psp_reference: str = Field(alias="pspReference")


class TransactionInitializeSessionEventSourceObjectCheckout(BaseModel):
    typename__: Literal["Checkout"] = Field(alias="__typename")
    typename__: Literal["Checkout"] = Field(alias="__typename")
    id: str
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    channel: "TransactionInitializeSessionEventSourceObjectCheckoutChannel"
    user_email: Optional[str] = Field(alias="userEmail")
    billing_address: Optional[
        "TransactionInitializeSessionEventSourceObjectCheckoutBillingAddress"
    ] = Field(alias="billingAddress")
    shipping_address: Optional[
        "TransactionInitializeSessionEventSourceObjectCheckoutShippingAddress"
    ] = Field(alias="shippingAddress")
    total: "TransactionInitializeSessionEventSourceObjectCheckoutTotal"
    typename__: Literal["Checkout"] = Field(alias="__typename")
    channel: "TransactionInitializeSessionEventSourceObjectCheckoutChannel"
    shipping_price: (
        "TransactionInitializeSessionEventSourceObjectCheckoutShippingPrice"
    ) = Field(alias="shippingPrice")
    delivery_method: Optional[
        Annotated[
            Union[
                "TransactionInitializeSessionEventSourceObjectCheckoutDeliveryMethodWarehouse",
                "TransactionInitializeSessionEventSourceObjectCheckoutDeliveryMethodShippingMethod",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="deliveryMethod")
    lines: List["TransactionInitializeSessionEventSourceObjectCheckoutLines"]


class TransactionInitializeSessionEventSourceObjectCheckoutChannel(BaseModel):
    id: str
    slug: str


class TransactionInitializeSessionEventSourceObjectCheckoutBillingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutShippingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutTotal(BaseModel):
    gross: "TransactionInitializeSessionEventSourceObjectCheckoutTotalGross"


class TransactionInitializeSessionEventSourceObjectCheckoutTotalGross(Money):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutShippingPrice(BaseModel):
    gross: "TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceGross"
    net: "TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceNet"
    tax: "TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceTax"


class TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceGross(Money):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceNet(Money):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceTax(Money):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutDeliveryMethodWarehouse(
    BaseModel
):
    typename__: Literal["Warehouse"] = Field(alias="__typename")


class TransactionInitializeSessionEventSourceObjectCheckoutDeliveryMethodShippingMethod(
    BaseModel
):
    typename__: Literal["ShippingMethod"] = Field(alias="__typename")
    id: str
    name: str


class TransactionInitializeSessionEventSourceObjectCheckoutLines(BaseModel):
    typename__: Literal["CheckoutLine"] = Field(alias="__typename")
    id: str
    quantity: int
    total_price: (
        "TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPrice"
    ) = Field(alias="totalPrice")
    checkout_variant: (
        "TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariant"
    ) = Field(alias="checkoutVariant")


class TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPrice(BaseModel):
    gross: "TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceGross"
    net: "TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceNet"
    tax: "TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceTax"


class TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceGross(Money):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceNet(Money):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceTax(Money):
    pass


class TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariant(
    BaseModel
):
    name: str
    sku: Optional[str]
    product: "TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProduct"


class TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProduct(
    BaseModel
):
    name: str
    thumbnail: Optional[
        "TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProductThumbnail"
    ]
    category: Optional[
        "TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProductCategory"
    ]


class TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProductThumbnail(
    BaseModel
):
    url: str


class TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProductCategory(
    BaseModel
):
    name: str


class TransactionInitializeSessionEventSourceObjectOrder(BaseModel):
    typename__: Literal["Order"] = Field(alias="__typename")
    typename__: Literal["Order"] = Field(alias="__typename")
    id: str
    language_code_enum: LanguageCodeEnum = Field(alias="languageCodeEnum")
    user_email: Optional[str] = Field(alias="userEmail")
    channel: "TransactionInitializeSessionEventSourceObjectOrderChannel"
    billing_address: Optional[
        "TransactionInitializeSessionEventSourceObjectOrderBillingAddress"
    ] = Field(alias="billingAddress")
    shipping_address: Optional[
        "TransactionInitializeSessionEventSourceObjectOrderShippingAddress"
    ] = Field(alias="shippingAddress")
    total: "TransactionInitializeSessionEventSourceObjectOrderTotal"
    typename__: Literal["Order"] = Field(alias="__typename")
    channel: "TransactionInitializeSessionEventSourceObjectOrderChannel"
    shipping_price: (
        "TransactionInitializeSessionEventSourceObjectOrderShippingPrice"
    ) = Field(alias="shippingPrice")
    delivery_method: Optional[
        Annotated[
            Union[
                "TransactionInitializeSessionEventSourceObjectOrderDeliveryMethodWarehouse",
                "TransactionInitializeSessionEventSourceObjectOrderDeliveryMethodShippingMethod",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="deliveryMethod")
    lines: List["TransactionInitializeSessionEventSourceObjectOrderLines"]


class TransactionInitializeSessionEventSourceObjectOrderChannel(BaseModel):
    id: str
    slug: str


class TransactionInitializeSessionEventSourceObjectOrderBillingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionInitializeSessionEventSourceObjectOrderShippingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionInitializeSessionEventSourceObjectOrderTotal(BaseModel):
    gross: "TransactionInitializeSessionEventSourceObjectOrderTotalGross"


class TransactionInitializeSessionEventSourceObjectOrderTotalGross(Money):
    pass


class TransactionInitializeSessionEventSourceObjectOrderShippingPrice(BaseModel):
    gross: "TransactionInitializeSessionEventSourceObjectOrderShippingPriceGross"
    net: "TransactionInitializeSessionEventSourceObjectOrderShippingPriceNet"
    tax: "TransactionInitializeSessionEventSourceObjectOrderShippingPriceTax"


class TransactionInitializeSessionEventSourceObjectOrderShippingPriceGross(Money):
    pass


class TransactionInitializeSessionEventSourceObjectOrderShippingPriceNet(Money):
    pass


class TransactionInitializeSessionEventSourceObjectOrderShippingPriceTax(Money):
    pass


class TransactionInitializeSessionEventSourceObjectOrderDeliveryMethodWarehouse(
    BaseModel
):
    typename__: Literal["Warehouse"] = Field(alias="__typename")


class TransactionInitializeSessionEventSourceObjectOrderDeliveryMethodShippingMethod(
    BaseModel
):
    typename__: Literal["ShippingMethod"] = Field(alias="__typename")
    id: str
    name: str


class TransactionInitializeSessionEventSourceObjectOrderLines(BaseModel):
    typename__: Literal["OrderLine"] = Field(alias="__typename")
    id: str
    quantity: int
    tax_rate: float = Field(alias="taxRate")
    total_price: "TransactionInitializeSessionEventSourceObjectOrderLinesTotalPrice" = (
        Field(alias="totalPrice")
    )
    order_variant: Optional[
        "TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariant"
    ] = Field(alias="orderVariant")


class TransactionInitializeSessionEventSourceObjectOrderLinesTotalPrice(BaseModel):
    gross: "TransactionInitializeSessionEventSourceObjectOrderLinesTotalPriceGross"
    net: "TransactionInitializeSessionEventSourceObjectOrderLinesTotalPriceNet"
    tax: "TransactionInitializeSessionEventSourceObjectOrderLinesTotalPriceTax"


class TransactionInitializeSessionEventSourceObjectOrderLinesTotalPriceGross(Money):
    pass


class TransactionInitializeSessionEventSourceObjectOrderLinesTotalPriceNet(Money):
    pass


class TransactionInitializeSessionEventSourceObjectOrderLinesTotalPriceTax(Money):
    pass


class TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariant(BaseModel):
    name: str
    sku: Optional[str]
    product: (
        "TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariantProduct"
    )


class TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariantProduct(
    BaseModel
):
    name: str
    thumbnail: Optional[
        "TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariantProductThumbnail"
    ]
    category: Optional[
        "TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariantProductCategory"
    ]


class TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariantProductThumbnail(
    BaseModel
):
    url: str


class TransactionInitializeSessionEventSourceObjectOrderLinesOrderVariantProductCategory(
    BaseModel
):
    name: str


class TransactionProcessSessionEvent(BaseModel):
    typename__: str = Field(alias="__typename")
    recipient: Optional["TransactionProcessSessionEventRecipient"]
    data: Optional[Any]
    merchant_reference: str = Field(alias="merchantReference")
    action: "TransactionProcessSessionEventAction"
    transaction: "TransactionProcessSessionEventTransaction"
    source_object: Union[
        "TransactionProcessSessionEventSourceObjectCheckout",
        "TransactionProcessSessionEventSourceObjectOrder",
    ] = Field(alias="sourceObject", discriminator="typename__")


class TransactionProcessSessionEventRecipient(PaymentGatewayRecipient):
    pass


class TransactionProcessSessionEventAction(BaseModel):
    amount: Any
    currency: str
    action_type: TransactionFlowStrategyEnum = Field(alias="actionType")


class TransactionProcessSessionEventTransaction(BaseModel):
    id: str
    psp_reference: str = Field(alias="pspReference")


class TransactionProcessSessionEventSourceObjectCheckout(BaseModel):
    typename__: Literal["Checkout"] = Field(alias="__typename")
    id: str
    language_code: LanguageCodeEnum = Field(alias="languageCode")
    user_email: Optional[str] = Field(alias="userEmail")
    billing_address: Optional[
        "TransactionProcessSessionEventSourceObjectCheckoutBillingAddress"
    ] = Field(alias="billingAddress")
    shipping_address: Optional[
        "TransactionProcessSessionEventSourceObjectCheckoutShippingAddress"
    ] = Field(alias="shippingAddress")
    typename__: Literal["Checkout"] = Field(alias="__typename")
    channel: "TransactionProcessSessionEventSourceObjectCheckoutChannel"
    shipping_price: (
        "TransactionProcessSessionEventSourceObjectCheckoutShippingPrice"
    ) = Field(alias="shippingPrice")
    delivery_method: Optional[
        Annotated[
            Union[
                "TransactionProcessSessionEventSourceObjectCheckoutDeliveryMethodWarehouse",
                "TransactionProcessSessionEventSourceObjectCheckoutDeliveryMethodShippingMethod",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="deliveryMethod")
    lines: List["TransactionProcessSessionEventSourceObjectCheckoutLines"]


class TransactionProcessSessionEventSourceObjectCheckoutBillingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutShippingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutChannel(BaseModel):
    id: str
    slug: str


class TransactionProcessSessionEventSourceObjectCheckoutShippingPrice(BaseModel):
    gross: "TransactionProcessSessionEventSourceObjectCheckoutShippingPriceGross"
    net: "TransactionProcessSessionEventSourceObjectCheckoutShippingPriceNet"
    tax: "TransactionProcessSessionEventSourceObjectCheckoutShippingPriceTax"


class TransactionProcessSessionEventSourceObjectCheckoutShippingPriceGross(Money):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutShippingPriceNet(Money):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutShippingPriceTax(Money):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutDeliveryMethodWarehouse(
    BaseModel
):
    typename__: Literal["Warehouse"] = Field(alias="__typename")


class TransactionProcessSessionEventSourceObjectCheckoutDeliveryMethodShippingMethod(
    BaseModel
):
    typename__: Literal["ShippingMethod"] = Field(alias="__typename")
    id: str
    name: str


class TransactionProcessSessionEventSourceObjectCheckoutLines(BaseModel):
    typename__: Literal["CheckoutLine"] = Field(alias="__typename")
    id: str
    quantity: int
    total_price: "TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPrice" = (
        Field(alias="totalPrice")
    )
    checkout_variant: (
        "TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariant"
    ) = Field(alias="checkoutVariant")


class TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPrice(BaseModel):
    gross: "TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceGross"
    net: "TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceNet"
    tax: "TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceTax"


class TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceGross(Money):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceNet(Money):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceTax(Money):
    pass


class TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariant(BaseModel):
    name: str
    sku: Optional[str]
    product: (
        "TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProduct"
    )


class TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProduct(
    BaseModel
):
    name: str
    thumbnail: Optional[
        "TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProductThumbnail"
    ]
    category: Optional[
        "TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProductCategory"
    ]


class TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProductThumbnail(
    BaseModel
):
    url: str


class TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProductCategory(
    BaseModel
):
    name: str


class TransactionProcessSessionEventSourceObjectOrder(BaseModel):
    typename__: Literal["Order"] = Field(alias="__typename")
    id: str
    language_code_enum: LanguageCodeEnum = Field(alias="languageCodeEnum")
    user_email: Optional[str] = Field(alias="userEmail")
    billing_address: Optional[
        "TransactionProcessSessionEventSourceObjectOrderBillingAddress"
    ] = Field(alias="billingAddress")
    shipping_address: Optional[
        "TransactionProcessSessionEventSourceObjectOrderShippingAddress"
    ] = Field(alias="shippingAddress")
    typename__: Literal["Order"] = Field(alias="__typename")
    channel: "TransactionProcessSessionEventSourceObjectOrderChannel"
    shipping_price: "TransactionProcessSessionEventSourceObjectOrderShippingPrice" = (
        Field(alias="shippingPrice")
    )
    delivery_method: Optional[
        Annotated[
            Union[
                "TransactionProcessSessionEventSourceObjectOrderDeliveryMethodWarehouse",
                "TransactionProcessSessionEventSourceObjectOrderDeliveryMethodShippingMethod",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="deliveryMethod")
    lines: List["TransactionProcessSessionEventSourceObjectOrderLines"]


class TransactionProcessSessionEventSourceObjectOrderBillingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionProcessSessionEventSourceObjectOrderShippingAddress(
    TransactionInitializeSessionAddress
):
    pass


class TransactionProcessSessionEventSourceObjectOrderChannel(BaseModel):
    id: str
    slug: str


class TransactionProcessSessionEventSourceObjectOrderShippingPrice(BaseModel):
    gross: "TransactionProcessSessionEventSourceObjectOrderShippingPriceGross"
    net: "TransactionProcessSessionEventSourceObjectOrderShippingPriceNet"
    tax: "TransactionProcessSessionEventSourceObjectOrderShippingPriceTax"


class TransactionProcessSessionEventSourceObjectOrderShippingPriceGross(Money):
    pass


class TransactionProcessSessionEventSourceObjectOrderShippingPriceNet(Money):
    pass


class TransactionProcessSessionEventSourceObjectOrderShippingPriceTax(Money):
    pass


class TransactionProcessSessionEventSourceObjectOrderDeliveryMethodWarehouse(BaseModel):
    typename__: Literal["Warehouse"] = Field(alias="__typename")


class TransactionProcessSessionEventSourceObjectOrderDeliveryMethodShippingMethod(
    BaseModel
):
    typename__: Literal["ShippingMethod"] = Field(alias="__typename")
    id: str
    name: str


class TransactionProcessSessionEventSourceObjectOrderLines(BaseModel):
    typename__: Literal["OrderLine"] = Field(alias="__typename")
    id: str
    quantity: int
    tax_rate: float = Field(alias="taxRate")
    total_price: "TransactionProcessSessionEventSourceObjectOrderLinesTotalPrice" = (
        Field(alias="totalPrice")
    )
    order_variant: Optional[
        "TransactionProcessSessionEventSourceObjectOrderLinesOrderVariant"
    ] = Field(alias="orderVariant")


class TransactionProcessSessionEventSourceObjectOrderLinesTotalPrice(BaseModel):
    gross: "TransactionProcessSessionEventSourceObjectOrderLinesTotalPriceGross"
    net: "TransactionProcessSessionEventSourceObjectOrderLinesTotalPriceNet"
    tax: "TransactionProcessSessionEventSourceObjectOrderLinesTotalPriceTax"


class TransactionProcessSessionEventSourceObjectOrderLinesTotalPriceGross(Money):
    pass


class TransactionProcessSessionEventSourceObjectOrderLinesTotalPriceNet(Money):
    pass


class TransactionProcessSessionEventSourceObjectOrderLinesTotalPriceTax(Money):
    pass


class TransactionProcessSessionEventSourceObjectOrderLinesOrderVariant(BaseModel):
    name: str
    sku: Optional[str]
    product: "TransactionProcessSessionEventSourceObjectOrderLinesOrderVariantProduct"


class TransactionProcessSessionEventSourceObjectOrderLinesOrderVariantProduct(
    BaseModel
):
    name: str
    thumbnail: Optional[
        "TransactionProcessSessionEventSourceObjectOrderLinesOrderVariantProductThumbnail"
    ]
    category: Optional[
        "TransactionProcessSessionEventSourceObjectOrderLinesOrderVariantProductCategory"
    ]


class TransactionProcessSessionEventSourceObjectOrderLinesOrderVariantProductThumbnail(
    BaseModel
):
    url: str


class TransactionProcessSessionEventSourceObjectOrderLinesOrderVariantProductCategory(
    BaseModel
):
    name: str


class TransactionRefundRequestedEvent(BaseModel):
    typename__: str = Field(alias="__typename")
    recipient: Optional["TransactionRefundRequestedEventRecipient"]
    action: "TransactionRefundRequestedEventAction"
    transaction: Optional["TransactionRefundRequestedEventTransaction"]


class TransactionRefundRequestedEventRecipient(PaymentGatewayRecipient):
    pass


class TransactionRefundRequestedEventAction(BaseModel):
    amount: Optional[Any]
    currency: str
    action_type: TransactionActionEnum = Field(alias="actionType")


class TransactionRefundRequestedEventTransaction(BaseModel):
    id: str
    psp_reference: str = Field(alias="pspReference")
    source_object: Optional[
        "TransactionRefundRequestedEventTransactionSourceObject"
    ] = Field(alias="sourceObject")


class TransactionRefundRequestedEventTransactionSourceObject(BaseModel):
    total: "TransactionRefundRequestedEventTransactionSourceObjectTotal"
    typename__: Literal["Order"] = Field(alias="__typename")
    channel: "TransactionRefundRequestedEventTransactionSourceObjectChannel"
    shipping_price: (
        "TransactionRefundRequestedEventTransactionSourceObjectShippingPrice"
    ) = Field(alias="shippingPrice")
    delivery_method: Optional[
        Annotated[
            Union[
                "TransactionRefundRequestedEventTransactionSourceObjectDeliveryMethodWarehouse",
                "TransactionRefundRequestedEventTransactionSourceObjectDeliveryMethodShippingMethod",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="deliveryMethod")
    lines: List["TransactionRefundRequestedEventTransactionSourceObjectLines"]


class TransactionRefundRequestedEventTransactionSourceObjectTotal(BaseModel):
    gross: "TransactionRefundRequestedEventTransactionSourceObjectTotalGross"


class TransactionRefundRequestedEventTransactionSourceObjectTotalGross(Money):
    pass


class TransactionRefundRequestedEventTransactionSourceObjectChannel(BaseModel):
    id: str
    slug: str


class TransactionRefundRequestedEventTransactionSourceObjectShippingPrice(BaseModel):
    gross: "TransactionRefundRequestedEventTransactionSourceObjectShippingPriceGross"
    net: "TransactionRefundRequestedEventTransactionSourceObjectShippingPriceNet"
    tax: "TransactionRefundRequestedEventTransactionSourceObjectShippingPriceTax"


class TransactionRefundRequestedEventTransactionSourceObjectShippingPriceGross(Money):
    pass


class TransactionRefundRequestedEventTransactionSourceObjectShippingPriceNet(Money):
    pass


class TransactionRefundRequestedEventTransactionSourceObjectShippingPriceTax(Money):
    pass


class TransactionRefundRequestedEventTransactionSourceObjectDeliveryMethodWarehouse(
    BaseModel
):
    typename__: Literal["Warehouse"] = Field(alias="__typename")


class TransactionRefundRequestedEventTransactionSourceObjectDeliveryMethodShippingMethod(
    BaseModel
):
    typename__: Literal["ShippingMethod"] = Field(alias="__typename")
    id: str
    name: str


class TransactionRefundRequestedEventTransactionSourceObjectLines(BaseModel):
    typename__: Literal["OrderLine"] = Field(alias="__typename")
    id: str
    quantity: int
    tax_rate: float = Field(alias="taxRate")
    total_price: (
        "TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPrice"
    ) = Field(alias="totalPrice")
    order_variant: Optional[
        "TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariant"
    ] = Field(alias="orderVariant")


class TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPrice(BaseModel):
    gross: "TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceGross"
    net: "TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceNet"
    tax: "TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceTax"


class TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceGross(Money):
    pass


class TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceNet(Money):
    pass


class TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceTax(Money):
    pass


class TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariant(
    BaseModel
):
    name: str
    sku: Optional[str]
    product: (
        "TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProduct"
    )


class TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProduct(
    BaseModel
):
    name: str
    thumbnail: Optional[
        "TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProductThumbnail"
    ]
    category: Optional[
        "TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProductCategory"
    ]


class TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProductThumbnail(
    BaseModel
):
    url: str


class TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProductCategory(
    BaseModel
):
    name: str


Address.model_rebuild()
Money.model_rebuild()
PaymentGatewayInitializeSessionAddress.model_rebuild()
PaymentGatewayRecipient.model_rebuild()
PaymentGatewayInitializeSessionEvent.model_rebuild()
TaxBaseLine.model_rebuild()
TaxDiscount.model_rebuild()
TaxBase.model_rebuild()
TransactionCancelationRequestedEvent.model_rebuild()
TransactionChargeRequestedEvent.model_rebuild()
TransactionInitializeSessionAddress.model_rebuild()
TransactionInitializeSessionEvent.model_rebuild()
TransactionProcessSessionEvent.model_rebuild()
TransactionRefundRequestedEvent.model_rebuild()
