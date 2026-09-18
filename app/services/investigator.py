from agents import Runner

from main import agent


def investigate_transaction(transaction_id: str) -> str:
    result = Runner.run_sync(
        agent,
        f"Investigate trade {transaction_id}.",
    )

    return result.final_output