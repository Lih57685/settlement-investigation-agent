from agents import Runner

from app.agent import agent
from app.models import InvestigationResult


def investigate_transaction(
    transaction_id: str,
) -> InvestigationResult:
    result = Runner.run_sync(
        agent,
        f"Investigate trade {transaction_id}.",
    )

    return result.final_output
