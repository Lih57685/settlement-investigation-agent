from fastapi import FastAPI, HTTPException
#from pydantic import BaseModel
from pydantic import BaseModel, field_validator
from app.models import InvestigationResponse
from app.services.investigator import investigate_transaction


app = FastAPI(
    title="Settlement Investigation Agent",
    version="0.1.0",
)


#class InvestigationRequest(BaseModel):
#    transaction_id: str

class InvestigationRequest(BaseModel):
    transaction_id: str

    @field_validator("transaction_id")
    @classmethod
    def validate_transaction_id(cls, value: str) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("transaction_id must not be blank")

        return normalized_value


@app.get("/health")
def health_check():
    return {"status": "ok"}

#@app.post("/investigate")
@app.post(
    "/investigate",
    response_model=InvestigationResponse,
)

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
    