"""AI-assisted dashboard tools (Review Center, Career Roadmap). Optional OpenAI; safe without key."""

from __future__ import annotations

import hashlib
import logging
import time
from datetime import date
from typing import Annotated, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.auth import get_current_user_id
from app.config import settings
from app.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ai-tools"])

# MVP in-process cache (24h) and daily usage cap per user
_CACHE: dict[str, tuple[float, str]] = {}
_CACHE_TTL_SEC = 24 * 3600
_DAILY_CAP = 10
_USAGE: dict[int, tuple[str, int]] = {}  # user_id -> (iso date, count)


def _cache_key(prefix: str, payload: str) -> str:
    h = hashlib.sha256(f"{prefix}:{payload}".encode()).hexdigest()
    return f"{prefix}:{h}"


def _get_cached(key: str) -> str | None:
    now = time.time()
    entry = _CACHE.get(key)
    if not entry:
        return None
    exp, text = entry
    if now > exp:
        del _CACHE[key]
        return None
    return text


def _set_cache(key: str, text: str) -> None:
    _CACHE[key] = (time.time() + _CACHE_TTL_SEC, text)


def _check_daily_cap(user_id: int) -> None:
    today = date.today().isoformat()
    d, c = _USAGE.get(user_id, ("", 0))
    if d != today:
        _USAGE[user_id] = (today, 0)
        c = 0
    if c >= _DAILY_CAP:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit of {_DAILY_CAP} AI requests reached. Try again tomorrow or use the Google search option.",
        )


def _bump_usage(user_id: int) -> None:
    today = date.today().isoformat()
    d, c = _USAGE.get(user_id, ("", 0))
    if d != today:
        c = 0
    _USAGE[user_id] = (today, c + 1)


REVIEW_CENTER_SYSTEM = """You are an education advisor helping a Filipino student choose a review center for scholarship or entrance exams.

Your task:
Provide a practical and honest guide to review centers near the student's location.

Include:
1. Specific review centers near the location (with nearby landmarks where possible)
2. Reputation and quality — passing rates if known, student feedback trends, strengths and weaknesses
3. Costs in PHP — typical fees, what is included
4. Timeline and structure — duration, schedule types (weekend/daily/hybrid)
5. Important deadlines — enrollment and exam-related timing
6. Comparison insights — when to choose one center over another
7. Free or alternative options — online/self-study paths

Be specific, practical, and honest. Avoid generic advice. Note uncertainty where data may be outdated.
If you lack verified data, say so and suggest how the student can verify locally.

Keep under 600 words."""


CAREER_SYSTEM = """You are a career advisor for Filipino students.

Your task:
Provide a realistic and practical career roadmap.

Include:
1. What the student will study — key subjects, real-world applications
2. Career paths — specific roles linked to the course
3. Day-to-day work — what professionals actually do
4. Salary expectations — Philippines vs international opportunities (ranges, caveats)
5. Hidden realities — skills not taught in school, industry expectations
6. What it takes to succeed — skills, habits, mindset
7. Self-assessment questions — help the student evaluate fit
8. Satisfaction and fit — who thrives in this field and why

Be honest and realistic, not overly optimistic. Avoid generic advice.

Keep under 700 words. Use clear section headings."""


def _call_openai(user_message: str, system_prompt: str) -> str:
    key = settings.openai_api_key
    if not key or not key.strip():
        raise HTTPException(status_code=503, detail="AI is not configured (missing OPENAI_API_KEY).")

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 2500,
        "temperature": 0.65,
    }
    try:
        with httpx.Client(timeout=60.0) as client:
            r = client.post(
                url,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json=payload,
            )
            r.raise_for_status()
            data = r.json()
            choice = data.get("choices", [{}])[0]
            msg = choice.get("message", {})
            content = msg.get("content") or ""
            if not content.strip():
                raise ValueError("empty response")
            return content.strip()
    except httpx.HTTPStatusError as e:
        logger.warning("OpenAI HTTP error: %s %s", e.response.status_code, e.response.text[:200])
        raise HTTPException(status_code=502, detail="AI provider returned an error. Try again or use Google search.") from e
    except Exception as e:
        logger.exception("OpenAI call failed")
        raise HTTPException(status_code=502, detail="Could not reach AI service. Try Google search instead.") from e


class ReviewCentersBody(BaseModel):
    location: str = Field(..., min_length=2, max_length=200)
    education_level: Optional[str] = Field(default=None, max_length=120)


class CareerRoadmapBody(BaseModel):
    course: str = Field(..., min_length=2, max_length=200)
    education_level: Optional[str] = Field(default=None, max_length=120)


class AiTextResponse(BaseModel):
    text: str
    from_ai: bool = True
    cached: bool = False


@router.post("/ai/review-centers", response_model=AiTextResponse)
@limiter.limit("20/minute")
def ai_review_centers(
    request: Request,
    body: ReviewCentersBody,
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    loc = body.location.strip()
    edu = (body.education_level or "").strip() or "not specified"
    cache_key = _cache_key("rc", f"{loc}|{edu}")
    hit = _get_cached(cache_key)
    if hit:
        return AiTextResponse(text=hit, from_ai=True, cached=True)

    _check_daily_cap(user_id)

    user_msg = f"""Student context:
* Location: {loc}
* Education level: {edu}

Provide the guide as specified in your instructions."""

    text = _call_openai(user_msg, REVIEW_CENTER_SYSTEM)
    _set_cache(cache_key, text)
    _bump_usage(user_id)
    return AiTextResponse(text=text, from_ai=True, cached=False)


@router.post("/ai/career-roadmap", response_model=AiTextResponse)
@limiter.limit("20/minute")
def ai_career_roadmap(
    request: Request,
    body: CareerRoadmapBody,
    user_id: Annotated[int | None, Depends(get_current_user_id)] = None,
):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    course = body.course.strip()
    edu = (body.education_level or "").strip() or "not specified"
    cache_key = _cache_key("cr", f"{course}|{edu}")
    hit = _get_cached(cache_key)
    if hit:
        return AiTextResponse(text=hit, from_ai=True, cached=True)

    _check_daily_cap(user_id)

    user_msg = f"""Student context:
* Course of interest: {course}
* Education level: {edu}
* Location: Philippines

Provide the roadmap as specified in your instructions."""

    text = _call_openai(user_msg, CAREER_SYSTEM)
    _set_cache(cache_key, text)
    _bump_usage(user_id)
    return AiTextResponse(text=text, from_ai=True, cached=False)
