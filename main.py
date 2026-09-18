import json

from dotenv import load_dotenv
from agents import Agent, Runner
from agents.decorators import tool

from db import (
    find_trade,
    find_settlement_status,
    find_ssi,
    find_error_logs,
)

load_dotenv()


# =========================================================
# Mock Database
# =========================================================


# =========================================================
# Tool 1: Trade Query
# =========================================================

@tool
def get_trade(trade_id: str) -> str:
    """
    Retrieve trade details for the specified trade ID.
    """

    print(f"\n[TOOL] get_trade({trade_id})")

    trade = find_trade(trade_id)

    if trade is None:
        return json.dumps(
            {
                "found": False,
                "trade_id": trade_id,
                "message": "Trade not found",
            }
        )

    return json.dumps(
        {
            "found": True,
            "trade": trade,
        },
        default=str,
    )


# =========================================================
# Tool 2: Settlement Status Query
# =========================================================

@tool
def get_settlement_status(trade_id: str) -> str:
    """
    Retrieve settlement status and failure reason for the trade.
    """

    print(f"\n[TOOL] get_settlement_status({trade_id})")

    settlement = find_settlement_status(trade_id)

    if settlement is None:
        return json.dumps(
            {
                "found": False,
                "trade_id": trade_id,
                "message": "Settlement information not found",
            }
        )

    return json.dumps(
        {
            "found": True,
            "settlement": settlement,
        },
        default=str,
    )

# =========================================================
# Tool 3: SSI Query
# =========================================================

@tool
def get_ssi(trade_id: str) -> str:
    """
    Retrieve internal and counterparty Standing Settlement Instructions
    for investigating an SSI mismatch.
    """

    print(f"\n[TOOL] get_ssi({trade_id})")

    ssi = find_ssi(trade_id)

    if ssi is None:
        return json.dumps(
            {
                "found": False,
                "trade_id": trade_id,
                "message": "SSI information not found",
            }
        )

    return json.dumps(
        {
            "found": True,
            "ssi": ssi,
        },
        default=str,
    )


@tool
def get_error_log(trade_id: str) -> str:
    """
    Retrieve system error logs related to settlement processing
    for the specified trade.
    """

    print(f"\n[TOOL] get_error_log({trade_id})")

    logs = find_error_logs(trade_id)

    if not logs:
        return json.dumps(
            {
                "found": False,
                "trade_id": trade_id,
                "message": "No relevant error log found",
            }
        )

    return json.dumps(
        {
            "found": True,
            "error_logs": logs,
        },
        default=str,
    )

# =========================================================
# Agent
# =========================================================

agent = Agent(
    name="Settlement Investigation Agent",

    instructions="""
You are a bank settlement investigation agent.

Your job is to investigate settlement failures using available tools.

Investigation policy:

1. Always start with get_trade.

2. If the trade does not exist:
   stop and report that the trade was not found.

3. If the trade status is SETTLED:
   report that settlement has completed.
   Do not perform unnecessary investigation.

4. If the trade is PENDING, FAILED, or otherwise unsettled:
   use get_settlement_status.

5. Examine reason_code carefully.

6. Select the next investigation tool based on evidence:

   - SSI_MISMATCH:
     use get_ssi.

   - SYSTEM_ERROR:
     use get_error_log.

7. For SSI_MISMATCH:
   compare internal_ssi and counterparty_ssi field by field
   and identify the exact mismatch.

8. For SYSTEM_ERROR:
   examine:
   - system
   - error_code
   - error message
   - retry count
   - last retry status

   Determine the likely technical root cause.

9. Only call tools that are relevant to the evidence.
   Do not perform unnecessary tool calls.

10. Never invent trade, settlement, SSI, or log data.

Final answer must include:

- Trade status
- Settlement status
- Failure category
- Evidence
- Root cause
- Recommended next action
""",

    tools=[
        get_trade,
        get_settlement_status,
        get_ssi,
        get_error_log,
    ],
)


# =========================================================
# Run
# =========================================================

def main():
    result = Runner.run_sync(
        agent,
        "Investigate trade TX9999."
    )

    print("\n")
    print("=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(result.final_output)


if __name__ == "__main__":
    main()