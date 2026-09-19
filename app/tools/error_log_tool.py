import json

from agents.decorators import tool

from db import find_error_logs


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
        {"found": True, "error_logs": logs},
        default=str,
    )
