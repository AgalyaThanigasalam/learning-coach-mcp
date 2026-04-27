"""
LLM integration — API key lives ONLY in backend .env
Uses Gemini 2.5 Flash (primary) with OpenAI fallback.
"""
import httpx, json, asyncio
from typing import Optional
from app.core.config import settings

# Use gemini-2.5-flash as primary (free tier available)
GEMINI_MODEL = "gemini-2.5-flash"

async def call_llm(system_prompt: str, user_prompt: str) -> Optional[str]:
    """Single entry point. Tries Gemini first, then OpenAI."""
    # Try Gemini first (more reliable free tier)
    if settings.GEMINI_API_KEY:
        result = await _gemini(system_prompt, user_prompt, settings.GEMINI_API_KEY)
        if result:
            return result

    # Fallback to OpenAI
    if settings.OPENAI_API_KEY and settings.LLM_PROVIDER == "openai":
        result = await _openai(system_prompt, user_prompt, settings.OPENAI_API_KEY)
        if result:
            return result

    return None

async def _gemini(system: str, user: str, key: str) -> Optional[str]:
    try:
        combined = f"{system}\n\n{user}"
        async with httpx.AsyncClient(timeout=25) as c:
            r = await c.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": combined}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 600}
                }
            )
            if r.status_code == 200:
                data = r.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            elif r.status_code == 429:
                print(f"Gemini rate limited, waiting 2s...")
                await asyncio.sleep(2)
                # retry once
                r2 = await c.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={key}",
                    headers={"Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": combined}]}],
                          "generationConfig": {"temperature": 0.7, "maxOutputTokens": 600}}
                )
                if r2.status_code == 200:
                    return r2.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                print(f"Gemini error {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"Gemini exception: {e}")
    return None

async def _openai(system: str, user: str, key: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=25) as c:
            r = await c.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo",
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user", "content": user}],
                      "temperature": 0.7, "max_tokens": 600}
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
            else:
                print(f"OpenAI error {r.status_code}")
    except Exception as e:
        print(f"OpenAI exception: {e}")
    return None

def is_llm_available() -> bool:
    return bool(settings.GEMINI_API_KEY or settings.OPENAI_API_KEY)
