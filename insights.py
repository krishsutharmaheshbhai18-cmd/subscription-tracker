"""
insights.py - this is where "AI" actually does something useful, instead of
just being a chatbot. We give Gemini the user's subscription LIST (structured
data) and ask it to reason over it: find duplicates, flag unused ones,
suggest savings.
"""
import json
import os
import re
from datetime import date, datetime

from dotenv import load_dotenv
from google import genai

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

PROMPT = """You are a personal finance assistant. Here is a list of a user's
active subscriptions as JSON. Today's date is {today}.

SUBSCRIPTIONS:
{subs_json}

Analyze them and return ONLY valid JSON with this exact shape:
{{
  "duplicate_categories": ["short note about overlapping subscriptions in the same category, if any"],
  "unused_warnings": ["short note about subscriptions not used in 30+ days, if any"],
  "savings_tips": ["short, specific money-saving suggestions, e.g. switch to yearly billing"],
  "summary": "one encouraging or informative sentence about their overall spending"
}}

If a category has nothing to report, return an empty list for it. Be specific
and mention subscription names. Do not invent subscriptions not in the list.
"""


def days_since(date_str: str) -> int:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (date.today() - d).days
    except Exception:
        return 0


def get_insights(subscriptions: list[dict]) -> dict:
    if not subscriptions:
        return {"duplicate_categories": [], "unused_warnings": [],
                "savings_tips": [], "summary": "Koi subscription add nahi hua abhi tak."}

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing. Create a .env file (see .env.example).")

    # Keep only the fields the model needs (smaller prompt, cheaper, faster)
    slim = [
        {
            "name": s["name"],
            "price": s["price"],
            "cycle": s["cycle"],
            "category": s["category"],
            "days_since_used": days_since(s.get("last_used") or str(date.today())),
        }
        for s in subscriptions
    ]

    client = genai.Client(api_key=key)
    prompt = PROMPT.format(today=date.today(), subs_json=json.dumps(slim, indent=2))
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    text = re.sub(r"^```(?:json)?|```$", "", response.text.strip(), flags=re.M).strip()
    return json.loads(text)
