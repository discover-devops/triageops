"""Talks to the AI model over HTTP, asynchronously, with a timeout and an API key."""
import httpx

from app.config import settings


async def ask_ai(complaint: str) -> dict:
    headers = {"Authorization": f"Bearer {settings.ai_api_key.get_secret_value()}"}
    async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
        response = await client.post(settings.ai_api_url, json={"complaint": complaint}, headers=headers)
        response.raise_for_status()
        return response.json()
