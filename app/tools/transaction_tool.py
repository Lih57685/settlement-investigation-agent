import json

from agents.decorators import tool

from db import find_trade


@tool
def get_trade(trade_id: str) -> str:
    """Retrieve trade details for the specified trade ID."""

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
        {"found": True, "trade": trade},
        default=str,
    )
