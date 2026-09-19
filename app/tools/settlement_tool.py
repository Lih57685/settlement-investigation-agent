import json

from agents.decorators import tool

from db import find_settlement_status


@tool
def get_settlement_status(trade_id: str) -> str:
    """Retrieve settlement status and failure reason for the trade."""

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
        {"found": True, "settlement": settlement},
        default=str,
    )
