import pytest
from pydantic import ValidationError


def test_status_enums_contain_only_allowed_values():
    from app.models import FailureCategory, SettlementStatus, TradeStatus

    assert {member.value for member in TradeStatus} == {
        "PENDING",
        "FAILED",
        "SETTLED",
        "NOT_FOUND",
    }
    assert {member.value for member in SettlementStatus} == {
        "FAILED",
        "SETTLED",
        "NOT_AVAILABLE",
    }
    assert {member.value for member in FailureCategory} == {
        "SSI_MISMATCH",
        "SYSTEM_ERROR",
        "NONE",
        "TRADE_NOT_FOUND",
    }


def test_investigation_result_accepts_allowed_status_values():
    from app.models import (
        FailureCategory,
        InvestigationResult,
        SettlementStatus,
        TradeStatus,
    )

    result = InvestigationResult(
        trade_status="SETTLED",
        settlement_status="SETTLED",
        failure_category="NONE",
        evidence=[],
        root_cause="Settlement completed",
        recommended_next_action="No action required",
    )

    assert result.trade_status is TradeStatus.SETTLED
    assert result.settlement_status is SettlementStatus.SETTLED
    assert result.failure_category is FailureCategory.NONE


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("failure_category", "None"),
        ("failure_category", "Trade not found"),
        ("settlement_status", "Settlement completed"),
        ("settlement_status", "Not available"),
    ],
)
def test_investigation_result_rejects_free_text_status_values(
    field,
    invalid_value,
):
    from app.models import InvestigationResult

    values = {
        "trade_status": "PENDING",
        "settlement_status": "FAILED",
        "failure_category": "SSI_MISMATCH",
        "evidence": [],
        "root_cause": "Pending investigation",
        "recommended_next_action": "Continue investigation",
    }
    values[field] = invalid_value

    with pytest.raises(ValidationError):
        InvestigationResult(**values)


def test_investigation_result_serializes_to_expected_structure():
    from app.models import (
        FailureCategory,
        InvestigationResult,
        SettlementStatus,
        TradeStatus,
    )

    result = InvestigationResult(
        trade_status=TradeStatus.PENDING,
        settlement_status=SettlementStatus.FAILED,
        failure_category=FailureCategory.SSI_MISMATCH,
        evidence=[
            "Internal account: 12345678",
            "Counterparty account: 87654321",
        ],
        root_cause="Settlement account mismatch",
        recommended_next_action=(
            "Confirm the correct SSI and retry settlement"
        ),
    )

    assert result.model_dump() == {
        "trade_status": "PENDING",
        "settlement_status": "FAILED",
        "failure_category": "SSI_MISMATCH",
        "evidence": [
            "Internal account: 12345678",
            "Counterparty account: 87654321",
        ],
        "root_cause": "Settlement account mismatch",
        "recommended_next_action": (
            "Confirm the correct SSI and retry settlement"
        ),
    }

def test_agent_uses_investigation_result_as_output_type():
    from app.models import InvestigationResult
    from app.agent import agent

    assert agent.output_type is InvestigationResult

def test_investigation_response_contains_transaction_and_result():
    from app.models import (
        FailureCategory,
        InvestigationResponse,
        InvestigationResult,
        SettlementStatus,
        TradeStatus,
    )

    result = InvestigationResult(
        trade_status=TradeStatus.PENDING,
        settlement_status=SettlementStatus.FAILED,
        failure_category=FailureCategory.SSI_MISMATCH,
        evidence=["Account numbers do not match"],
        root_cause="Settlement account mismatch",
        recommended_next_action="Confirm SSI and retry settlement",
    )

    response = InvestigationResponse(
        transaction_id="TX1001",
        result=result,
    )

    assert response.model_dump() == {
        "transaction_id": "TX1001",
        "result": {
            "trade_status": "PENDING",
            "settlement_status": "FAILED",
            "failure_category": "SSI_MISMATCH",
            "evidence": ["Account numbers do not match"],
            "root_cause": "Settlement account mismatch",
            "recommended_next_action": (
                "Confirm SSI and retry settlement"
            ),
        },
    }
