from __future__ import annotations
import json
import os
import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("CHAT_MODEL", "llama3:8b")

SYSTEM_PROMPT = """You are an assistant that summarizes meeting transcripts for busy professionals.

Given a transcript, produce a concise, accurate summary. Do not invent details that are not in the transcript.

Respond with ONLY a valid JSON object in exactly this shape, and nothing else:

{
  "overview": "A 2-3 sentence plain-language summary of what the meeting was about.",
  "decisions": ["Each key decision made, as a short string.", "..."],
  "action_items": [
    {"task": "What needs to be done", "owner": "Who is responsible, or 'Unassigned'"}
  ]
}

If a section has nothing, use an empty list. Do not include any text outside the JSON."""

def summarize_transcript(transcript: str) -> dict:
    resp = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Summarize this meeting transcript:\n\n{transcript}"},
            ],
            "stream": False,
            "format": "json",
        },
        timeout=300,
    )
    resp.raise_for_status()
    raw = resp.json()["message"]["content"].strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            data = json.loads(raw[start:end + 1])
        else:
            raise ValueError(f"Model did not return valid JSON. Got: {raw[:200]}")
    return {
        "overview": data.get("overview", ""),
        "decisions": data.get("decisions", []),
        "action_items": data.get("action_items", []),
    }
