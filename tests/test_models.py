def test_investigation_result_serializes_to_expected_structure():
    from app.models import InvestigationResult

    result = InvestigationResult(
        trade_status="PENDING",
        settlement_status="FAILED",
        failure_category="SSI_MISMATCH",
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
    from app.models import InvestigationResponse, InvestigationResult

    result = InvestigationResult(
        trade_status="PENDING",
        settlement_status="FAILED",
        failure_category="SSI_MISMATCH",
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
