__all__ = [
    "CALCULATE_TAXES_GQL",
    "CHECK_APP_TOKEN_GQL",
    "PAYMENT_GATEWAY_INITIALIZE_SESSION_GQL",
    "TRANSACTION_CANCELATION_REQUESTED_GQL",
    "TRANSACTION_CHARGE_REQUESTED_GQL",
    "TRANSACTION_EVENT_REPORT_GQL",
    "TRANSACTION_INITIALIZE_SESSION_GQL",
    "TRANSACTION_PROCESS_SESSION_GQL",
    "TRANSACTION_REFUND_REQUESTED_GQL",
]

TRANSACTION_EVENT_REPORT_GQL = """
mutation TransactionEventReport($transactionId: ID!, $amount: PositiveDecimal!, $availableActions: [TransactionActionEnum!]!, $externalUrl: String!, $message: String, $pspReference: String!, $time: DateTime!, $type: TransactionEventTypeEnum!) {
  transactionEventReport(
    id: $transactionId
    amount: $amount
    availableActions: $availableActions
    externalUrl: $externalUrl
    message: $message
    pspReference: $pspReference
    time: $time
    type: $type
  ) {
    alreadyProcessed
    errors {
      field
      message
      code
    }
  }
}
"""

CHECK_APP_TOKEN_GQL = """
query checkAppToken {
  app {
    id
  }
}
"""

CALCULATE_TAXES_GQL = """
subscription CalculateTaxes {
  event {
    ...CalculateTaxesEvent
  }
}

fragment Address on Address {
  streetAddress1
  streetAddress2
  city
  countryArea
  postalCode
  country {
    code
  }
}

fragment CalculateTaxesEvent on Event {
  __typename
  ... on CalculateTaxes {
    taxBase {
      ...TaxBase
    }
    recipient {
      privateMetadata {
        key
        value
      }
    }
  }
}

fragment Money on Money {
  currency
  amount
}

fragment TaxBase on TaxableObject {
  pricesEnteredWithTax
  currency
  channel {
    slug
  }
  discounts {
    ...TaxDiscount
  }
  address {
    ...Address
  }
  shippingPrice {
    ...Money
  }
  lines {
    ...TaxBaseLine
  }
}

fragment TaxBaseLine on TaxableObjectLine {
  sourceLine {
    __typename
    ... on CheckoutLine {
      id
      checkoutProductVariant: variant {
        id
        product {
          taxClass {
            id
            name
          }
        }
      }
    }
    ... on OrderLine {
      id
      orderProductVariant: variant {
        id
        product {
          taxClass {
            id
            name
          }
        }
      }
    }
  }
  quantity
  unitPrice {
    amount
  }
  totalPrice {
    ...Money
  }
  productSku
}

fragment TaxDiscount on TaxableObjectDiscount {
  name
  amount {
    amount
  }
}
"""

PAYMENT_GATEWAY_INITIALIZE_SESSION_GQL = """
subscription PaymentGatewayInitializeSession {
  event {
    __typename
    ...PaymentGatewayInitializeSessionEvent
  }
}

fragment Money on Money {
  currency
  amount
}

fragment PaymentGatewayInitializeSessionAddress on Address {
  country {
    code
  }
}

fragment PaymentGatewayInitializeSessionEvent on PaymentGatewayInitializeSession {
  __typename
  recipient {
    ...PaymentGatewayRecipient
  }
  data
  amount
  issuingPrincipal {
    ... on Node {
      id
    }
  }
  sourceObject {
    __typename
    ... on Checkout {
      id
      channel {
        id
        slug
      }
      languageCode
      billingAddress {
        ...PaymentGatewayInitializeSessionAddress
      }
      total: totalPrice {
        gross {
          ...Money
        }
      }
    }
    ... on Order {
      id
      channel {
        id
        slug
      }
      languageCodeEnum
      userEmail
      billingAddress {
        ...PaymentGatewayInitializeSessionAddress
      }
      total {
        gross {
          ...Money
        }
      }
    }
  }
}

fragment PaymentGatewayRecipient on App {
  id
  privateMetadata {
    key
    value
  }
  metadata {
    key
    value
  }
}
"""

TRANSACTION_CANCELATION_REQUESTED_GQL = """
subscription TransactionCancelationRequested {
  event {
    __typename
    ...TransactionCancelationRequestedEvent
  }
}

fragment PaymentGatewayRecipient on App {
  id
  privateMetadata {
    key
    value
  }
  metadata {
    key
    value
  }
}

fragment TransactionCancelationRequestedEvent on TransactionCancelationRequested {
  __typename
  recipient {
    ...PaymentGatewayRecipient
  }
  action {
    actionType
    currency
    amount
  }
  transaction {
    id
    pspReference
    sourceObject: order {
      channel {
        id
        slug
      }
    }
  }
}
"""

TRANSACTION_CHARGE_REQUESTED_GQL = """
subscription TransactionChargeRequested {
  event {
    __typename
    ...TransactionChargeRequestedEvent
  }
}

fragment Money on Money {
  currency
  amount
}

fragment OrderOrCheckoutLines on OrderOrCheckout {
  __typename
  ... on Checkout {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      checkoutVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
  ... on Order {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      taxRate
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      orderVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
}

fragment PaymentGatewayRecipient on App {
  id
  privateMetadata {
    key
    value
  }
  metadata {
    key
    value
  }
}

fragment TransactionChargeRequestedEvent on TransactionChargeRequested {
  __typename
  recipient {
    ...PaymentGatewayRecipient
  }
  action {
    amount
    currency
    actionType
  }
  transaction {
    id
    pspReference
    sourceObject: order {
      ... on Order {
        total {
          gross {
            ...Money
          }
        }
      }
      ...OrderOrCheckoutLines
    }
  }
}
"""

TRANSACTION_INITIALIZE_SESSION_GQL = """
subscription TransactionInitializeSession {
  event {
    __typename
    ...TransactionInitializeSessionEvent
  }
}

fragment Money on Money {
  currency
  amount
}

fragment OrderOrCheckoutLines on OrderOrCheckout {
  __typename
  ... on Checkout {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      checkoutVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
  ... on Order {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      taxRate
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      orderVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
}

fragment OrderOrCheckoutSourceObject on OrderOrCheckout {
  __typename
  ... on Checkout {
    id
    languageCode
    channel {
      id
      slug
    }
    userEmail: email
    billingAddress {
      ...TransactionInitializeSessionAddress
    }
    shippingAddress {
      ...TransactionInitializeSessionAddress
    }
    total: totalPrice {
      gross {
        ...Money
      }
    }
    ...OrderOrCheckoutLines
  }
  ... on Order {
    id
    languageCodeEnum
    userEmail
    channel {
      id
      slug
    }
    billingAddress {
      ...TransactionInitializeSessionAddress
    }
    shippingAddress {
      ...TransactionInitializeSessionAddress
    }
    total {
      gross {
        ...Money
      }
    }
    ...OrderOrCheckoutLines
  }
}

fragment PaymentGatewayRecipient on App {
  id
  privateMetadata {
    key
    value
  }
  metadata {
    key
    value
  }
}

fragment TransactionInitializeSessionAddress on Address {
  firstName
  lastName
  phone
  city
  streetAddress1
  streetAddress2
  postalCode
  countryArea
  companyName
  country {
    code
  }
}

fragment TransactionInitializeSessionEvent on TransactionInitializeSession {
  __typename
  recipient {
    ...PaymentGatewayRecipient
  }
  data
  merchantReference
  action {
    amount
    currency
    actionType
  }
  issuingPrincipal {
    __typename
    ... on Node {
      id
    }
  }
  transaction {
    id
    pspReference
  }
  sourceObject {
    __typename
    ...OrderOrCheckoutSourceObject
  }
}
"""

TRANSACTION_PROCESS_SESSION_GQL = """
subscription TransactionProcessSession {
  event {
    __typename
    ...TransactionProcessSessionEvent
  }
}

fragment Money on Money {
  currency
  amount
}

fragment OrderOrCheckoutLines on OrderOrCheckout {
  __typename
  ... on Checkout {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      checkoutVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
  ... on Order {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      taxRate
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      orderVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
}

fragment PaymentGatewayRecipient on App {
  id
  privateMetadata {
    key
    value
  }
  metadata {
    key
    value
  }
}

fragment TransactionInitializeSessionAddress on Address {
  firstName
  lastName
  phone
  city
  streetAddress1
  streetAddress2
  postalCode
  countryArea
  companyName
  country {
    code
  }
}

fragment TransactionProcessSessionEvent on TransactionProcessSession {
  __typename
  recipient {
    ...PaymentGatewayRecipient
  }
  data
  merchantReference
  action {
    amount
    currency
    actionType
  }
  transaction {
    id
    pspReference
  }
  sourceObject {
    __typename
    ... on Checkout {
      id
      languageCode
      userEmail: email
      billingAddress {
        ...TransactionInitializeSessionAddress
      }
      shippingAddress {
        ...TransactionInitializeSessionAddress
      }
      ...OrderOrCheckoutLines
    }
    ... on Order {
      id
      languageCodeEnum
      userEmail
      billingAddress {
        ...TransactionInitializeSessionAddress
      }
      shippingAddress {
        ...TransactionInitializeSessionAddress
      }
      ...OrderOrCheckoutLines
    }
  }
}
"""

TRANSACTION_REFUND_REQUESTED_GQL = """
subscription TransactionRefundRequested {
  event {
    __typename
    ...TransactionRefundRequestedEvent
  }
}

fragment Money on Money {
  currency
  amount
}

fragment OrderOrCheckoutLines on OrderOrCheckout {
  __typename
  ... on Checkout {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      checkoutVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
  ... on Order {
    channel {
      id
      slug
    }
    shippingPrice {
      gross {
        ...Money
      }
      net {
        ...Money
      }
      tax {
        ...Money
      }
    }
    deliveryMethod {
      __typename
      ... on ShippingMethod {
        id
        name
      }
    }
    lines {
      __typename
      id
      quantity
      taxRate
      totalPrice {
        gross {
          ...Money
        }
        net {
          ...Money
        }
        tax {
          ...Money
        }
      }
      orderVariant: variant {
        name
        sku
        product {
          name
          thumbnail {
            url
          }
          category {
            name
          }
        }
      }
    }
  }
}

fragment PaymentGatewayRecipient on App {
  id
  privateMetadata {
    key
    value
  }
  metadata {
    key
    value
  }
}

fragment TransactionRefundRequestedEvent on TransactionRefundRequested {
  __typename
  recipient {
    ...PaymentGatewayRecipient
  }
  action {
    amount
    currency
    actionType
  }
  transaction {
    id
    pspReference
    sourceObject: order {
      ... on Order {
        total {
          gross {
            ...Money
          }
        }
      }
      ...OrderOrCheckoutLines
    }
  }
}
"""
