
import os, json
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def parse_questions_with_gemini(extracted_text):
    from gemini_call_stub import gemini_api_call  # Replace with real Gemini API call

    system_prompt = """
    You are an assistant that extracts multiple-choice questions from text.
    Return strict JSON array:
    [
      {
        "q": "<question text>",
        "options": ["A text","B text","C text","D text"],
        "answer": "A"|"B"|"C"|"D",
        "solution": "<solution text>"
      }
    ]
    Only JSON, no extra text.
    """
    user_prompt = f"{extracted_text}\n\nExtract all questions with options, answer and solution."

    resp_text = gemini_api_call(system_prompt + "\n" + user_prompt)
    return json.loads(resp_text)