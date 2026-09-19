from pydantic import BaseModel


class InvestigationResult(BaseModel):
    trade_status: str
    settlement_status: str
    failure_category: str
    evidence: list[str]
    root_cause: str
    recommended_next_action: str

class InvestigationResponse(BaseModel):
    transaction_id: str
    result: InvestigationResult