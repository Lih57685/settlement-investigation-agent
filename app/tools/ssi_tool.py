import json

from agents.decorators import tool

from db import find_ssi


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
        {"found": True, "ssi": ssi},
        default=str,
    )
