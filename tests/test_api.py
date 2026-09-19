from fastapi.testclient import TestClient

import app.api as api_module


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