class StripeError(Exception):
    "Base Stripe Exception"


class CannotCalculateTaxForZeroNetValueError(StripeError):
    "Cannot calculate tax for zero checkout/order net value."
