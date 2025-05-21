from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import TransactionEventReportErrorCode


class TransactionEventReport(BaseModel):
    transaction_event_report: Optional[
        "TransactionEventReportTransactionEventReport"
    ] = Field(alias="transactionEventReport")


class TransactionEventReportTransactionEventReport(BaseModel):
    already_processed: Optional[bool] = Field(alias="alreadyProcessed")
    errors: List["TransactionEventReportTransactionEventReportErrors"]


class TransactionEventReportTransactionEventReportErrors(BaseModel):
    field: Optional[str]
    message: Optional[str]
    code: TransactionEventReportErrorCode


TransactionEventReport.model_rebuild()
TransactionEventReportTransactionEventReport.model_rebuild()
