"""The AI decides. The contract checks. Anything wrong goes to Human Review."""
import httpx
from pydantic import ValidationError

from app.ai_client import ask_ai
from app.models import Category, Team, TriageResponse, TriageResult

HUMAN_REVIEW = dict(category=Category.unknown, priority=2, team=Team.human_review)


async def ai_triage(complaint: str) -> TriageResponse:
    try:
        raw_answer = await ask_ai(complaint)
    except httpx.TimeoutException:
        return TriageResponse(**HUMAN_REVIEW, decided_by="fallback: AI timed out")
    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        return TriageResponse(**HUMAN_REVIEW, decided_by=f"fallback: AI returned {status}")
    except httpx.HTTPError:
        return TriageResponse(**HUMAN_REVIEW, decided_by="fallback: AI unavailable")

    try:
        result = TriageResult.model_validate(raw_answer)
    except ValidationError:
        return TriageResponse(**HUMAN_REVIEW, decided_by="fallback: invalid AI answer")

    return TriageResponse(**result.model_dump(), decided_by="ai")
