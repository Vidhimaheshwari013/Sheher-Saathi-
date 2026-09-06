import json
from .groq_client import get_groq_client
from .prompts import EXTRACTION_SYSTEM_PROMPT

def extract_complaint(raw_text: str) -> dict:
    client = get_groq_client()

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
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