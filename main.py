import os
import requests
from flask import Flask, request, jsonify
from ocr_utils import extract_text_from_pdf
from gemini_utils import extract_questions_from_ai

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
BOT = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)

def send_poll(chat_id, q, options, correct):
    params = {
        "chat_id": chat_id,
        "question": q,
        "options": json.dumps(options),
        "type": "quiz",
        "correct_option_id": correct
    }
    requests.post(f"{BOT}/sendPoll", data=params)

def download_file(file_id):
    file_path = requests.get(f"{BOT}/getFile?file_id={file_id}").json()['result']['file_path']
    return requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}").content

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json
    msg = update.get("message", {})
    
    if "document" in msg:
        chat_id = msg["chat"]["id"]
        file_id = msg["document"]["file_id"]

        requests.post(f"{BOT}/sendMessage", json={"chat_id": chat_id, "text": "📄 Processing PDF…"})

        pdf_bytes = download_file(file_id)
        pdf_path = "/tmp/file.pdf"
        open(pdf_path, "wb").write(pdf_bytes)

        text = extract_text_from_pdf(pdf_path)

        questions = extract_questions_from_ai(text)

        for i, q in enumerate(questions):
            send_poll(
                chat_id,
                f"{i+1}/{len(questions)}: {q['q']}",
                q["options"],
                q["answer_index"]
            )

        return jsonify({"ok": True})

    return jsonify({"ok": True})