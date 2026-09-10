import json
from .groq_client import get_groq_client
from .prompts import EXTRACTION_SYSTEM_PROMPT
from .prompts import SUMMARY_SYSTEM_PROMPT
import re

def extract_complaint(raw_text: str) -> dict:
    client = get_groq_client()

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        max_tokens=500,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "issues": [],
            "language": "unknown",
            "needs_followup": True,
            "followup_question": "Could you describe the issue again in a bit more detail?",
        }


def summarize_cluster(raw_texts: list) -> str:
    client = get_groq_client()
    combined = "\n".join(f"- {t}" for t in raw_texts)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": f"Reports:\n{combined}"},
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()
    

