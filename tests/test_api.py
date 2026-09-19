from fastapi.testclient import TestClient

import app.api as api_module
import pytest

client = TestClient(api_module.app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_investigate_returns_agent_result(monkeypatch):
    def fake_investigate_transaction(transaction_id: str) -> str:
        assert transaction_id == "TX1001"
        return "Investigation completed"

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
        "result": "Investigation completed",
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