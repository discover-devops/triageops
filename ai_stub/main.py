"""A fake AI model. It answers like a real model would, but costs nothing.

STUB_DELAY    seconds to wait before answering (default 1.0), like a real model thinking
STUB_MODE     normal = sensible answers, bad = the wrong answer from our story
STUB_API_KEY  if set, callers must send "Authorization: Bearer <key>", like a real AI provider
"""
import asyncio
import os

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="AI Stub")

DELAY = float(os.getenv("STUB_DELAY", "1.0"))
MODE = os.getenv("STUB_MODE", "normal")
API_KEY = os.getenv("STUB_API_KEY", "")


@app.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok", "mode": MODE, "delay": DELAY}


@app.post("/classify")
async def classify(body: dict, authorization: str = Header(default="")) -> dict:
    if API_KEY and authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="invalid API key")

    await asyncio.sleep(DELAY)

    if MODE == "bad":
        return {"category": "payment", "priority": "High", "team": "payment team"}

    text = str(body.get("complaint", "")).lower()
    if "charged" in text or "payment" in text or "upi" in text:
        return {"category": "payments", "priority": 4, "team": "payments"}
    if "refund" in text:
        return {"category": "refund", "priority": 3, "team": "refunds"}
    if "late" in text or "delivery" in text or "rider" in text:
        return {"category": "delivery", "priority": 3, "team": "delivery_ops"}
    if "cold" in text or "missing" in text or "restaurant" in text:
        return {"category": "restaurant", "priority": 2, "team": "restaurant_support"}
    return {"category": "unknown", "priority": 2, "team": "human_review"}
