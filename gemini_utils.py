# gemini_utils.py
import os, json, time
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def parse_questions_with_gemini(extracted_text):
    # Craft a clear prompt instructing Gemini to return strict JSON
    system_prompt = """
    You are an assistant that extracts multiple-choice questions from a block of text.
    Return a JSON array, each element:
    {
      "q": "<question text>",
      "options": ["A text","B text","C text","D text"],
      "answer": "A" or "B" or "C" or "D",
      "solution": "<solution text>"
    }
    Ensure valid JSON only.
    """
    user_prompt = f"{extracted_text}\n\nExtract all questions with options, answer and solution."

    # ===== Replace below with your Gemini API call code =====
    # Example: call OpenAI-like API. For now, assume a function gemini_api_call(prompt)->str
    from gemini_call_stub import gemini_api_call
    resp_text = gemini_api_call(system_prompt + "\n" + user_prompt)
    # Try to parse JSON
    data = json.loads(resp_text)
    return data