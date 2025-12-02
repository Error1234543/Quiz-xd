
import requests

API_KEY = "YOUR_GEMINI_API_KEY"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY

def extract_questions_from_ai(text):
    prompt = f"""
Extract all MCQ in Gujarati.
Output strictly in JSON:
[
 {{"q":"...", "options":["A","B","C","D"], "answer_index":0}},
]
Text:
{text}
"""

    res = requests.post(URL, json={"contents":[{"parts":[{"text":prompt}]}]})
    out = res.json()["candidates"][0]["content"]["parts"][0]["text"]

    import json
    return json.loads(out)