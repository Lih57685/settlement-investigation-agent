from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.investigator import investigate_transaction


app = FastAPI(
    title="Settlement Investigation Agent",
    version="0.1.0",
)


class InvestigationRequest(BaseModel):
    transaction_id: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/investigate")
def investigate(request: InvestigationRequest):
    try:
        result = investigate_transaction(request.transaction_id)

        return {
            "transaction_id": request.transaction_id,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
    