"""Complaint Triage Service: contract, async AI call, configuration, secret, JSON logs, health check."""
import time
import uuid

from fastapi import FastAPI, Response

from app.config import settings
from app.logging_config import setup_logging
from app.models import ComplaintIn, TriageResponse
from app.triage import ai_triage

log = setup_logging(settings.log_level)
app = FastAPI(title="Complaint Triage Service", version="1.2.0")

log.info("service_starting", extra={"fields": {
    "version": app.version,
    "environment": settings.environment,
    "ai_api_url": settings.ai_api_url,
    "ai_timeout_seconds": settings.ai_timeout_seconds,
}})


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok", "version": app.version, "environment": settings.environment}


@app.post("/triage", response_model=TriageResponse)
async def triage(body: ComplaintIn, response: Response) -> TriageResponse:
    request_id = uuid.uuid4().hex[:12]
    start = time.perf_counter()

    result = await ai_triage(body.complaint)

    duration_ms = round((time.perf_counter() - start) * 1000)
    response.headers["X-Request-ID"] = request_id
    log.info("triage_completed", extra={"fields": {
        "request_id": request_id,
        "order_id": body.order_id,
        "complaint_length": len(body.complaint),
        "category": result.category.value,
        "priority": result.priority,
        "team": result.team.value,
        "decided_by": result.decided_by,
        "duration_ms": duration_ms,
    }})
    return result
