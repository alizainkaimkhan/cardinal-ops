"""FastAPI application entrypoint. Dev server: uv run uvicorn main:app --reload"""

import uuid

from fastapi import FastAPI

from schemas import Envelope, HealthData

app = FastAPI(title="CardinalOps API")


@app.get("/health", response_model=Envelope[HealthData])
def health() -> Envelope[HealthData]:
    return Envelope[HealthData](
        data=HealthData(status="ok", version="0.1.0"),
        trace_id=str(uuid.uuid4()),
    )
