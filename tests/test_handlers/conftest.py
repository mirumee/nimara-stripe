import pytest

import graphql_client as gql
from nimara_stripe.services.saleor.config import StripeConfig, StripeSaleorConfigData


@pytest.fixture(scope="function")
def saleor_test_calculate_tax_event():
    return gql.CalculateTaxesEventCalculateTaxes(
        __typename="CalculateTaxes",
        taxBase=gql.CalculateTaxesEventCalculateTaxesTaxBase(
            pricesEnteredWithTax=True,
            currency="PLN",
            channel=gql.TaxBaseChannel(slug="test_channel_slug"),
            discounts=[],
            address=gql.TaxBaseAddress(
                streetAddress1="Street address 1",
                streetAddress2="Street address 2",
                city="Warsaw",
                countryArea="",
                postalCode="00-001",
                country=gql.AddressCountry(code="PL"),
            ),
            shippingPrice=gql.TaxBaseShippingPrice(currency="PLN", amount=10.0),
            lines=[
                gql.TaxBaseLines(
                    sourceLine=gql.TaxBaseLineSourceLineCheckoutLine(
                        __typename="CheckoutLine",
                        id="test_line_id",
                        checkoutProductVariant=gql.TaxBaseLineSourceLineCheckoutLineCheckoutProductVariant(
                            id="test_variant_id",
                            product=gql.TaxBaseLineSourceLineCheckoutLineCheckoutProductVariantProduct(
                                taxClass=None
                            ),
                        ),
                    ),
                    quantity=1,
                    unitPrice=gql.TaxBaseLineUnitPrice(amount=1000.0),
                    totalPrice=gql.TaxBaseLineTotalPrice(amount=1000.0, currency="PLN"),
                    productSku="testSku",
                )
            ],
        ),
        recipient=gql.CalculateTaxesEventCalculateTaxesRecipient(
            privateMetadata=[
                gql.CalculateTaxesEventCalculateTaxesRecipientPrivateMetadata(
                    key="testKey", value="testValue"
                )
            ]
        ),
    )


@pytest.fixture(scope="function")
def saleor_config_data():
    return StripeSaleorConfigData(
        auth_token="test_auth_token",
        saleor_domain="test_saleor_domain",
        saleor_app_id="test_app_id",
        stripe_configurations_for_channels={
            "test_channel_1": StripeConfig(
                stripe_pub_key="test_stripe_pub_key_1",
                stripe_secret_key="test_stripe_secret_key_1",
                stripe_webhook_secret_key="stripe_webhook_secret_key_1",
            ),
            "test_channel_2": StripeConfig(
                stripe_pub_key="test_stripe_pub_key_2",
                stripe_secret_key="test_stripe_secret_key_2",
                stripe_webhook_secret_key="stripe_webhook_secret_key_2",
            ),
        },
    )


@pytest.fixture(scope="function")
def stripe_config():
    return StripeConfig(
        stripe_pub_key="test_stripe_pub_key_1",
        stripe_secret_key="test_stripe_secret_key_1",
        stripe_webhook_secret_key="stripe_webhook_secret_key_1",
    )


@pytest.fixture(scope="function")
def stripe_webhook_payment_intent_created_body():
    return {
        "id": "evt_xxx",
        "object": "event",
        "api_version": "2015-10-16",
        "created": 1730918312,
        "data": {
            "object": {
                "id": "pi_3QIlKGH0QBbcHXEP04EXBKGp",
                "object": "payment_intent",
                "allowed_source_types": ["card", "link", "paypal"],
                "amount": 30000,
                "amount_capturable": 0,
                "amount_details": {"tip": {}},
                "amount_received": 0,
                "application": None,
                "application_fee_amount": None,
                "automatic_payment_methods": {
                    "allow_redirects": "always",
                    "enabled": True,
                },
                "canceled_at": None,
                "cancellation_reason": None,
                "capture_method": "automatic",
                "charges": {
                    "object": "list",
                    "data": [],
                    "has_more": False,
                    "total_count": 0,
                    "url": "/v1/charges?payment_intent=pi_3QIlKGH0QBbcHXEP04EXBKGp",
                },
                "client_secret": "pi_3QIlKGH0QBbcHXEP04EXBKGp_secret_Gl9eLFgWVB1r21uQpzki69zmZ",
                "confirmation_method": "automatic",
                "created": 1731045944,
                "currency": "usd",
                "customer": None,
                "description": None,
                "invoice": None,
                "last_payment_error": None,
                "latest_charge": None,
                "livemode": False,
                "metadata": {
                    "channelId": "Q2hhbm5lbDox",
                    "channelSlug": "default-channel",
                    "saleorDomain": "test_saleor_domain",
                    "transactionId": "VHJhbnNhY3Rpb25JdGVtOjI1MzlhZmYxLWM4NTUtNGEyNi04OWI4LWY4N2M4MzYxMTNkYg==",  # noqa: E501
                },
                "next_action": None,
                "next_source_action": None,
                "on_behalf_of": None,
                "payment_method": None,
                "payment_method_configuration_details": {
                    "id": "pmc_1OyCi4H0QBbcHXEP56fosA67",
                    "parent": None,
                },
                "payment_method_options": {
                    "card": {
                        "installments": None,
                        "mandate_options": None,
                        "network": None,
                        "request_three_d_secure": "automatic",
                    },
                    "link": {"persistent_token": None},
                    "paypal": {"preferred_locale": None, "reference": None},
                },
                "payment_method_types": ["card", "link", "paypal"],
                "processing": None,
                "receipt_email": None,
                "review": None,
                "setup_future_usage": None,
                "shipping": None,
                "source": None,
                "statement_descriptor": None,
                "statement_descriptor_suffix": None,
                "status": "requires_source",
                "transfer_data": None,
                "transfer_group": None,
            }
        },
        "livemode": False,
        "pending_webhooks": 0,
        "request": "req_xxx",
        "type": "payment_intent.created",
    }


@pytest.fixture
def payment_gateway_initialize_session_event():
    return gql.PaymentGatewayInitializeSessionEvent(
        __typename="App",
        recipient=gql.PaymentGatewayInitializeSessionEventRecipient(
            id="recipient_123",
            privateMetadata=[
                gql.PaymentGatewayRecipientPrivateMetadata(key="key1", value="value1")
            ],
            metadata=[gql.PaymentGatewayRecipientMetadata(key="meta1", value="value1")],
        ),
        data={"custom": "example"},
        amount={"amount": 123.45, "currency": "USD"},
        issuingPrincipal=gql.PaymentGatewayInitializeSessionEventIssuingPrincipalApp(
            __typename="App",
            id="app_456",
        ),
        sourceObject=gql.PaymentGatewayInitializeSessionEventSourceObjectCheckout(
            __typename="Checkout",
            id="checkout_789",
            channel=gql.PaymentGatewayInitializeSessionEventSourceObjectCheckoutChannel(
                id="channel_001", slug="default-channel"
            ),
            languageCode=gql.LanguageCodeEnum.EN,
            billingAddress=gql.PaymentGatewayInitializeSessionEventSourceObjectCheckoutBillingAddress(
                country=gql.PaymentGatewayInitializeSessionAddressCountry(code="US")
            ),
            total=gql.PaymentGatewayInitializeSessionEventSourceObjectCheckoutTotal(
                gross=gql.PaymentGatewayInitializeSessionEventSourceObjectCheckoutTotalGross(
                    currency="USD", amount=150.00
                )
            ),
        ),
    )


@pytest.fixture
def transaction_initialize_session_event():
    return gql.TransactionInitializeSessionEvent(
        __typename="Checkout",
        recipient=gql.TransactionInitializeSessionEventRecipient(
            id="recipient_123",
            privateMetadata=[],
            metadata=[],
        ),
        data={"key": "value"},
        merchantReference="order-123",
        action=gql.TransactionInitializeSessionEventAction(
            amount=200.00,
            currency="USD",
            actionType=gql.TransactionFlowStrategyEnum.CHARGE,
        ),
        issuingPrincipal=gql.TransactionInitializeSessionEventIssuingPrincipalUser(
            __typename="User", id="user_789"
        ),
        transaction=gql.TransactionInitializeSessionEventTransaction(
            id="transaction_456", pspReference="psp-abc-123"
        ),
        sourceObject=gql.TransactionInitializeSessionEventSourceObjectCheckout(
            __typename="Checkout",
            id="checkout_001",
            languageCode=gql.LanguageCodeEnum.EN,
            userEmail="customer@example.com",
            channel=gql.TransactionInitializeSessionEventSourceObjectCheckoutChannel(
                id="channel_01", slug="default-channel"
            ),
            billingAddress=gql.TransactionInitializeSessionEventSourceObjectCheckoutBillingAddress(
                firstName="John",
                lastName="Doe",
                phone="+123456789",
                city="New York",
                streetAddress1="123 Main St",
                streetAddress2="Apt 4",
                postalCode="10001",
                countryArea="NY",
                companyName="Example Inc",
                country=gql.TransactionInitializeSessionAddressCountry(code="US"),
            ),
            shippingAddress=gql.TransactionInitializeSessionEventSourceObjectCheckoutShippingAddress(
                firstName="John",
                lastName="Doe",
                phone="+123456789",
                city="New York",
                streetAddress1="123 Main St",
                streetAddress2="Apt 4",
                postalCode="10001",
                countryArea="NY",
                companyName="Example Inc",
                country=gql.TransactionInitializeSessionAddressCountry(code="US"),
            ),
            total=gql.TransactionInitializeSessionEventSourceObjectCheckoutTotal(
                gross=gql.TransactionInitializeSessionEventSourceObjectCheckoutTotalGross(
                    currency="USD", amount=200.00
                )
            ),
            shippingPrice=gql.TransactionInitializeSessionEventSourceObjectCheckoutShippingPrice(
                gross=gql.TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceGross(
                    currency="USD", amount=10.00
                ),
                net=gql.TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceNet(
                    currency="USD", amount=8.00
                ),
                tax=gql.TransactionInitializeSessionEventSourceObjectCheckoutShippingPriceTax(
                    currency="USD", amount=2.00
                ),
            ),
            deliveryMethod=None,
            lines=[
                gql.TransactionInitializeSessionEventSourceObjectCheckoutLines(
                    __typename="CheckoutLine",
                    id="line_1",
                    quantity=2,
                    totalPrice=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPrice(
                        gross=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceGross(
                            currency="USD", amount=100.00
                        ),
                        net=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceNet(
                            currency="USD", amount=80.00
                        ),
                        tax=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesTotalPriceTax(
                            currency="USD", amount=20.00
                        ),
                    ),
                    checkoutVariant=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariant(
                        name="M-size Shirt",
                        sku="SKU12345",
                        product=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProduct(
                            name="Cool Shirt",
                            thumbnail=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProductThumbnail(
                                url="https://example.com/media/shirt.jpg"
                            ),
                            category=gql.TransactionInitializeSessionEventSourceObjectCheckoutLinesCheckoutVariantProductCategory(
                                name="T-Shirts"
                            ),
                        ),
                    ),
                )
            ],
        ),
    )


@pytest.fixture
def transaction_process_session_event():
    return gql.TransactionProcessSessionEvent(
        __typename="Checkout",
        recipient=gql.TransactionProcessSessionEventRecipient(
            id="recipient_456",
            privateMetadata=[],
            metadata=[],
        ),
        data={"info": "processing step"},
        merchantReference="order-456",
        action=gql.TransactionProcessSessionEventAction(
            amount=250.00,
            currency="USD",
            actionType=gql.TransactionFlowStrategyEnum.CHARGE,
        ),
        transaction=gql.TransactionProcessSessionEventTransaction(
            id="txn_789", pspReference="psp-xyz-789"
        ),
        sourceObject=gql.TransactionProcessSessionEventSourceObjectCheckout(
            __typename="Checkout",
            id="checkout_789",
            languageCode=gql.LanguageCodeEnum.EN,
            userEmail="customer2@example.com",
            billingAddress=gql.TransactionProcessSessionEventSourceObjectCheckoutBillingAddress(
                firstName="Alice",
                lastName="Smith",
                phone="+1987654321",
                city="Los Angeles",
                streetAddress1="456 Sunset Blvd",
                streetAddress2="",
                postalCode="90001",
                countryArea="CA",
                companyName="Example Corp",
                country=gql.TransactionInitializeSessionAddressCountry(code="US"),
            ),
            shippingAddress=gql.TransactionProcessSessionEventSourceObjectCheckoutShippingAddress(
                firstName="Alice",
                lastName="Smith",
                phone="+1987654321",
                city="Los Angeles",
                streetAddress1="456 Sunset Blvd",
                streetAddress2="",
                postalCode="90001",
                countryArea="CA",
                companyName="Example Corp",
                country=gql.TransactionInitializeSessionAddressCountry(code="US"),
            ),
            channel=gql.TransactionProcessSessionEventSourceObjectCheckoutChannel(
                id="channel_002", slug="us-channel"
            ),
            shippingPrice=gql.TransactionProcessSessionEventSourceObjectCheckoutShippingPrice(
                gross=gql.TransactionProcessSessionEventSourceObjectCheckoutShippingPriceGross(
                    currency="USD", amount=12.00
                ),
                net=gql.TransactionProcessSessionEventSourceObjectCheckoutShippingPriceNet(
                    currency="USD", amount=10.00
                ),
                tax=gql.TransactionProcessSessionEventSourceObjectCheckoutShippingPriceTax(
                    currency="USD", amount=2.00
                ),
            ),
            deliveryMethod=None,
            lines=[
                gql.TransactionProcessSessionEventSourceObjectCheckoutLines(
                    __typename="CheckoutLine",
                    id="line_002",
                    quantity=1,
                    totalPrice=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPrice(
                        gross=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceGross(
                            currency="USD", amount=238.00
                        ),
                        net=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceNet(
                            currency="USD", amount=190.00
                        ),
                        tax=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesTotalPriceTax(
                            currency="USD", amount=48.00
                        ),
                    ),
                    checkoutVariant=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariant(
                        name="Fancy Pants",
                        sku="SKU-9988",
                        product=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProduct(
                            name="Designer Pants",
                            thumbnail=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProductThumbnail(
                                url="https://example.com/media/pants.jpg"
                            ),
                            category=gql.TransactionProcessSessionEventSourceObjectCheckoutLinesCheckoutVariantProductCategory(
                                name="Pants"
                            ),
                        ),
                    ),
                )
            ],
        ),
    )


@pytest.fixture
def transaction_charge_requested_event():
    return gql.TransactionChargeRequestedEvent(
        __typename="Checkout",
        recipient=gql.TransactionChargeRequestedEventRecipient(
            id="recipient_999",
            privateMetadata=[],
            metadata=[],
        ),
        action=gql.TransactionChargeRequestedEventAction(
            amount=300.00,
            currency="USD",
            actionType=gql.TransactionActionEnum.CHARGE,
        ),
        transaction=gql.TransactionChargeRequestedEventTransaction(
            id="txn_123456",
            pspReference="psp-456-xyz",
            sourceObject=gql.TransactionChargeRequestedEventTransactionSourceObject(
                __typename="Order",
                channel=gql.TransactionChargeRequestedEventTransactionSourceObjectChannel(
                    id="channel-003", slug="us-store"
                ),
                total=gql.TransactionChargeRequestedEventTransactionSourceObjectTotal(
                    gross=gql.TransactionChargeRequestedEventTransactionSourceObjectTotalGross(
                        currency="USD", amount=300.00
                    )
                ),
                shippingPrice=gql.TransactionChargeRequestedEventTransactionSourceObjectShippingPrice(
                    gross=gql.TransactionChargeRequestedEventTransactionSourceObjectShippingPriceGross(
                        currency="USD", amount=15.00
                    ),
                    net=gql.TransactionChargeRequestedEventTransactionSourceObjectShippingPriceNet(
                        currency="USD", amount=12.00
                    ),
                    tax=gql.TransactionChargeRequestedEventTransactionSourceObjectShippingPriceTax(
                        currency="USD", amount=3.00
                    ),
                ),
                deliveryMethod=gql.TransactionChargeRequestedEventTransactionSourceObjectDeliveryMethodShippingMethod(
                    __typename="ShippingMethod",
                    id="ship-method-001",
                    name="Standard Shipping",
                ),
                lines=[
                    gql.TransactionChargeRequestedEventTransactionSourceObjectLines(
                        __typename="OrderLine",
                        id="line-xyz",
                        quantity=1,
                        taxRate=0.2,
                        totalPrice=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPrice(
                            gross=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceGross(
                                currency="USD", amount=285.00
                            ),
                            net=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceNet(
                                currency="USD", amount=237.50
                            ),
                            tax=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesTotalPriceTax(
                                currency="USD", amount=47.50
                            ),
                        ),
                        orderVariant=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariant(
                            name="Elegant Coat",
                            sku="COAT-7890",
                            product=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProduct(
                                name="Winter Coat",
                                thumbnail=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProductThumbnail(
                                    url="https://example.com/media/coat.jpg"
                                ),
                                category=gql.TransactionChargeRequestedEventTransactionSourceObjectLinesOrderVariantProductCategory(
                                    name="Outerwear"
                                ),
                            ),
                        ),
                    )
                ],
            ),
        ),
    )


@pytest.fixture
def transaction_cancellation_requested_event():
    return gql.TransactionCancelationRequestedEvent(
        __typename="Order",
        recipient=gql.TransactionCancelationRequestedEventRecipient(
            id="recipient_555",
            privateMetadata=[],
            metadata=[],
        ),
        action=gql.TransactionCancelationRequestedEventAction(
            actionType=gql.TransactionActionEnum.CANCEL,
            currency="USD",
            amount=None,  # lub np. 0.0
        ),
        transaction=gql.TransactionCancelationRequestedEventTransaction(
            id="txn_cancel_001",
            pspReference="psp-cancel-abc123",
            sourceObject=gql.TransactionCancelationRequestedEventTransactionSourceObject(
                channel=gql.TransactionCancelationRequestedEventTransactionSourceObjectChannel(
                    id="channel_cancel_001", slug="cancel-channel"
                )
            ),
        ),
    )


@pytest.fixture
def transaction_refund_requested_event():
    return gql.TransactionRefundRequestedEvent(
        __typename="Order",
        recipient=gql.TransactionRefundRequestedEventRecipient(
            id="recipient_888",
            privateMetadata=[],
            metadata=[],
        ),
        action=gql.TransactionRefundRequestedEventAction(
            amount=180.00,
            currency="USD",
            actionType=gql.TransactionActionEnum.REFUND,
        ),
        transaction=gql.TransactionRefundRequestedEventTransaction(
            id="txn_refund_001",
            pspReference="psp-refund-456abc",
            sourceObject=gql.TransactionRefundRequestedEventTransactionSourceObject(
                __typename="Order",
                channel=gql.TransactionRefundRequestedEventTransactionSourceObjectChannel(
                    id="channel_refund_01", slug="refund-channel"
                ),
                total=gql.TransactionRefundRequestedEventTransactionSourceObjectTotal(
                    gross=gql.TransactionRefundRequestedEventTransactionSourceObjectTotalGross(
                        currency="USD", amount=180.00
                    )
                ),
                shippingPrice=gql.TransactionRefundRequestedEventTransactionSourceObjectShippingPrice(
                    gross=gql.TransactionRefundRequestedEventTransactionSourceObjectShippingPriceGross(
                        currency="USD", amount=10.00
                    ),
                    net=gql.TransactionRefundRequestedEventTransactionSourceObjectShippingPriceNet(
                        currency="USD", amount=8.00
                    ),
                    tax=gql.TransactionRefundRequestedEventTransactionSourceObjectShippingPriceTax(
                        currency="USD", amount=2.00
                    ),
                ),
                deliveryMethod=gql.TransactionRefundRequestedEventTransactionSourceObjectDeliveryMethodShippingMethod(
                    __typename="ShippingMethod",
                    id="shipping-method-refund-001",
                    name="Express Return",
                ),
                lines=[
                    gql.TransactionRefundRequestedEventTransactionSourceObjectLines(
                        __typename="OrderLine",
                        id="line_refund_001",
                        quantity=1,
                        taxRate=0.2,
                        totalPrice=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPrice(
                            gross=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceGross(
                                currency="USD", amount=170.00
                            ),
                            net=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceNet(
                                currency="USD", amount=141.67
                            ),
                            tax=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesTotalPriceTax(
                                currency="USD", amount=28.33
                            ),
                        ),
                        orderVariant=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariant(
                            name="Red Hoodie",
                            sku="HOODIE-001",
                            product=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProduct(
                                name="Stylish Red Hoodie",
                                thumbnail=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProductThumbnail(
                                    url="https://example.com/media/hoodie.jpg"
                                ),
                                category=gql.TransactionRefundRequestedEventTransactionSourceObjectLinesOrderVariantProductCategory(
                                    name="Hoodies"
                                ),
                            ),
                        ),
                    )
                ],
            ),
        ),
    )
