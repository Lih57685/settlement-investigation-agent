import builtins
import importlib
import sys


def test_investigate_transaction_calls_existing_agent(monkeypatch):
    from app.services import investigator

    calls = {}

    class FakeResult:
        final_output = "Investigation completed"

    class FakeRunner:
        @staticmethod
        def run_sync(selected_agent, prompt):
            calls["agent"] = selected_agent
            calls["prompt"] = prompt
            return FakeResult()

    fake_agent = object()

    monkeypatch.setattr(investigator, "Runner", FakeRunner, raising=False)
    monkeypatch.setattr(investigator, "agent", fake_agent, raising=False)

    result = investigator.investigate_transaction("TX1001")

    assert result == "Investigation completed"
    assert calls["agent"] is fake_agent
    assert calls["prompt"] == "Investigate trade TX1001."

def test_investigate_transaction_declares_structured_return_type():
    from typing import get_type_hints

    from app.models import InvestigationResult
    from app.services.investigator import investigate_transaction

    return_type = get_type_hints(
        investigate_transaction
    )["return"]

    assert return_type is InvestigationResult


def test_investigator_does_not_import_main(monkeypatch):
    real_import = builtins.__import__

    def import_without_main(name, *args, **kwargs):
        if name == "main":
            raise AssertionError("investigator must not import main")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_without_main)
    sys.modules.pop("app.services.investigator", None)

    investigator = importlib.import_module("app.services.investigator")

    assert investigator.agent is not None
