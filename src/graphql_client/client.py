from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, List, Optional, Union

from .async_base_client import AsyncBaseClient
from .base_model import UNSET
from .operations import (
    CALCULATE_TAXES_GQL,
    CHECK_APP_TOKEN_GQL,
    PAYMENT_GATEWAY_INITIALIZE_SESSION_GQL,
    TRANSACTION_CANCELATION_REQUESTED_GQL,
    TRANSACTION_CHARGE_REQUESTED_GQL,
    TRANSACTION_EVENT_REPORT_GQL,
    TRANSACTION_INITIALIZE_SESSION_GQL,
    TRANSACTION_PROCESS_SESSION_GQL,
    TRANSACTION_REFUND_REQUESTED_GQL,
)

if TYPE_CHECKING:
    from .base_model import UnsetType
    from .calculate_taxes import (
        CalculateTaxesEventCalculateTaxes,
        CalculateTaxesEventEvent,
    )
    from .check_app_token import CheckAppTokenApp
    from .enums import TransactionActionEnum, TransactionEventTypeEnum
    from .payment_gateway_initialize_session import (
        PaymentGatewayInitializeSessionEventEvent,
        PaymentGatewayInitializeSessionEventPaymentGatewayInitializeSession,
    )
    from .transaction_cancelation_requested import (
        TransactionCancelationRequestedEventEvent,
        TransactionCancelationRequestedEventTransactionCancelationRequested,
    )
    from .transaction_charge_requested import (
        TransactionChargeRequestedEventEvent,
        TransactionChargeRequestedEventTransactionChargeRequested,
    )
    from .transaction_event_report import TransactionEventReportTransactionEventReport
    from .transaction_initialize_session import (
        TransactionInitializeSessionEventEvent,
        TransactionInitializeSessionEventTransactionInitializeSession,
    )
    from .transaction_process_session import (
        TransactionProcessSessionEventEvent,
        TransactionProcessSessionEventTransactionProcessSession,
    )
    from .transaction_refund_requested import (
        TransactionRefundRequestedEventEvent,
        TransactionRefundRequestedEventTransactionRefundRequested,
    )


def gql(q: str) -> str:
    return q


class AutoGenClient(AsyncBaseClient):
    async def transaction_event_report(
        self,
        transaction_id: str,
        amount: Any,
        available_actions: List["TransactionActionEnum"],
        external_url: str,
        psp_reference: str,
        time: Any,
        type: "TransactionEventTypeEnum",
        message: Union[Optional[str], "UnsetType"] = UNSET,
        **kwargs: Any
    ) -> Optional["TransactionEventReportTransactionEventReport"]:
        from .transaction_event_report import TransactionEventReport

        variables: Dict[str, object] = {
            "transactionId": transaction_id,
            "amount": amount,
            "availableActions": available_actions,
            "externalUrl": external_url,
            "message": message,
            "pspReference": psp_reference,
            "time": time,
            "type": type,
        }
        response = await self.execute(
            query=TRANSACTION_EVENT_REPORT_GQL,
            operation_name="TransactionEventReport",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return TransactionEventReport.model_validate(data).transaction_event_report

    async def check_app_token(self, **kwargs: Any) -> Optional["CheckAppTokenApp"]:
        from .check_app_token import CheckAppToken

        variables: Dict[str, object] = {}
        response = await self.execute(
            query=CHECK_APP_TOKEN_GQL,
            operation_name="checkAppToken",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CheckAppToken.model_validate(data).app

    async def calculate_taxes(
        self, **kwargs: Any
    ) -> AsyncIterator[
        Optional[Union["CalculateTaxesEventEvent", "CalculateTaxesEventCalculateTaxes"]]
    ]:
        from .calculate_taxes import CalculateTaxes

        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=CALCULATE_TAXES_GQL,
            operation_name="CalculateTaxes",
            variables=variables,
            **kwargs
        ):
            yield CalculateTaxes.model_validate(data).event

    async def payment_gateway_initialize_session(self, **kwargs: Any) -> AsyncIterator[
        Optional[
            Union[
                "PaymentGatewayInitializeSessionEventEvent",
                "PaymentGatewayInitializeSessionEventPaymentGatewayInitializeSession",
            ]
        ]
    ]:
        from .payment_gateway_initialize_session import PaymentGatewayInitializeSession

        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=PAYMENT_GATEWAY_INITIALIZE_SESSION_GQL,
            operation_name="PaymentGatewayInitializeSession",
            variables=variables,
            **kwargs
        ):
            yield PaymentGatewayInitializeSession.model_validate(data).event

    async def transaction_cancelation_requested(self, **kwargs: Any) -> AsyncIterator[
        Optional[
            Union[
                "TransactionCancelationRequestedEventEvent",
                "TransactionCancelationRequestedEventTransactionCancelationRequested",
            ]
        ]
    ]:
        from .transaction_cancelation_requested import TransactionCancelationRequested

        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=TRANSACTION_CANCELATION_REQUESTED_GQL,
            operation_name="TransactionCancelationRequested",
            variables=variables,
            **kwargs
        ):
            yield TransactionCancelationRequested.model_validate(data).event

    async def transaction_charge_requested(self, **kwargs: Any) -> AsyncIterator[
        Optional[
            Union[
                "TransactionChargeRequestedEventEvent",
                "TransactionChargeRequestedEventTransactionChargeRequested",
            ]
        ]
    ]:
        from .transaction_charge_requested import TransactionChargeRequested

        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=TRANSACTION_CHARGE_REQUESTED_GQL,
            operation_name="TransactionChargeRequested",
            variables=variables,
            **kwargs
        ):
            yield TransactionChargeRequested.model_validate(data).event

    async def transaction_initialize_session(self, **kwargs: Any) -> AsyncIterator[
        Optional[
            Union[
                "TransactionInitializeSessionEventEvent",
                "TransactionInitializeSessionEventTransactionInitializeSession",
            ]
        ]
    ]:
        from .transaction_initialize_session import TransactionInitializeSession

        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=TRANSACTION_INITIALIZE_SESSION_GQL,
            operation_name="TransactionInitializeSession",
            variables=variables,
            **kwargs
        ):
            yield TransactionInitializeSession.model_validate(data).event

    async def transaction_process_session(self, **kwargs: Any) -> AsyncIterator[
        Optional[
            Union[
                "TransactionProcessSessionEventEvent",
                "TransactionProcessSessionEventTransactionProcessSession",
            ]
        ]
    ]:
        from .transaction_process_session import TransactionProcessSession

        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=TRANSACTION_PROCESS_SESSION_GQL,
            operation_name="TransactionProcessSession",
            variables=variables,
            **kwargs
        ):
            yield TransactionProcessSession.model_validate(data).event

    async def transaction_refund_requested(self, **kwargs: Any) -> AsyncIterator[
        Optional[
            Union[
                "TransactionRefundRequestedEventEvent",
                "TransactionRefundRequestedEventTransactionRefundRequested",
            ]
        ]
    ]:
        from .transaction_refund_requested import TransactionRefundRequested

        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=TRANSACTION_REFUND_REQUESTED_GQL,
            operation_name="TransactionRefundRequested",
            variables=variables,
            **kwargs
        ):
            yield TransactionRefundRequested.model_validate(data).event
