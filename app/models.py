from enum import StrEnum

from pydantic import BaseModel


class TradeStatus(StrEnum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    SETTLED = "SETTLED"
    NOT_FOUND = "NOT_FOUND"


class SettlementStatus(StrEnum):
    FAILED = "FAILED"
    SETTLED = "SETTLED"
    NOT_AVAILABLE = "NOT_AVAILABLE"


class FailureCategory(StrEnum):
    SSI_MISMATCH = "SSI_MISMATCH"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    NONE = "NONE"
    TRADE_NOT_FOUND = "TRADE_NOT_FOUND"


class InvestigationResult(BaseModel):
    trade_status: TradeStatus
    settlement_status: SettlementStatus
    failure_category: FailureCategory
    evidence: list[str]
    root_cause: str
    recommended_next_action: str


class InvestigationResponse(BaseModel):
    transaction_id: str
    result: InvestigationResult
