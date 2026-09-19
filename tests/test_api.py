from fastapi.testclient import TestClient

import app.api as api_module
import pytest

client = TestClient(api_module.app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_investigate_returns_agent_result(monkeypatch):
    from app.models import (
        FailureCategory,
        InvestigationResult,
        SettlementStatus,
        TradeStatus,
    )

    def fake_investigate_transaction(
        transaction_id: str,
    ) -> InvestigationResult:
        assert transaction_id == "TX1001"

        return InvestigationResult(
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

    monkeypatch.setattr(
        api_module,
        "investigate_transaction",
        fake_investigate_transaction,
    )

    response = client.post(
        "/investigate",
        json={"transaction_id": "TX1001"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "transaction_id": "TX1001",
        "result": {
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
        },
    }
    
@pytest.mark.parametrize(
    "transaction_id",
    [
        "",
        "   ",
    ],
)
def test_investigate_rejects_blank_transaction_id(
    monkeypatch,
    transaction_id,
):
    calls = []

    def fake_investigate_transaction(received_transaction_id: str) -> str:
        calls.append(received_transaction_id)
        return "This must not be called"

    monkeypatch.setattr(
        api_module,
        "investigate_transaction",
        fake_investigate_transaction,
    )

    response = client.post(
        "/investigate",
        json={"transaction_id": transaction_id},
    )

    assert response.status_code == 422
    assert calls == []

def test_investigate_declares_structured_response_model():
    from app.models import InvestigationResponse

    investigate_route = next(
        route
        for route in api_module.app.routes
        if route.path == "/investigate"
        and "POST" in route.methods
    )

    assert investigate_route.response_model is InvestigationResponse
