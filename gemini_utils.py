import requests
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def parse_questions_with_gemini(text):
    """
    Send extracted text to Gemini AI to find:
    - Questions
    - Options A/B/C/D
    - Correct answer
    - Solution
    Returns JSON list:
    [
      {"q": ..., "options": [...], "answer": ..., "solution": ...},
      ...
    ]
    """
    prompt = f"""
Extract all questions from this text.
Format JSON:
[
  {{
    "q": "Question text",
    "options": ["A text", "B text", "C text", "D text"],
    "answer": "A/B/C/D",
    "solution": "Solution text"
  }},
  ...
]
Keep text exactly as in PDF.
Text:
{text}
"""

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gemini",
        "prompt": prompt,
        "max_tokens": 3000
    }

    response = requests.post("https://api.gemini.ai/v1/generate", headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    # Assuming AI returns JSON string in 'text' field
    return json.loads(result["text"])