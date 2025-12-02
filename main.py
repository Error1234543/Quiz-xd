import os
import json
import requests
from flask import Flask, request, jsonify
from ocr_utils import extract_text_from_pdf
from gemini_utils import parse_questions_with_gemini
from html_generator import build_html_from_questions

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)

def download_file(file_id):
    r = requests.get(f"{BOT_URL}/getFile", params={"file_id": file_id})
    r.raise_for_status()
    file_info = r.json()
    file_path = file_info["result"]["file_path"]
    download_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    rr = requests.get(download_url)
    rr.raise_for_status()
    return rr.content

def send_message(chat_id, text):
    requests.post(f"{BOT_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def send_document(chat_id, filename, content_bytes):
    files = {"document": (filename, content_bytes)}
    data = {"chat_id": chat_id}
    requests.post(f"{BOT_URL}/sendDocument", data=data, files=files)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return jsonify({"ok": False}), 400

    msg = data.get("message") or data.get("edited_message")
    if not msg:
        return jsonify({"ok": True})

    chat_id = msg["chat"]["id"]

    doc = msg.get("document")
    if doc:
        filename = doc.get("file_name", "file.pdf")
        file_id = doc["file_id"]

        send_message(chat_id, "Processing your PDF — started OCR & parsing. 🛠️")

        try:
            file_bytes = download_file(file_id)
        except Exception as e:
            send_message(chat_id, f"Failed to download file: {e}")
            return jsonify({"ok": False}), 500

        tmp_pdf = f"/tmp/{filename}"
        with open(tmp_pdf, "wb") as f:
            f.write(file_bytes)

        try:
            extracted_text = extract_text_from_pdf(tmp_pdf)
        except Exception as e:
            send_message(chat_id, f"OCR failed: {e}")
            return jsonify({"ok": False}), 500

        send_message(chat_id, "OCR done — sending text to Gemini AI for answers...")

        try:
            questions_json = parse_questions_with_gemini(extracted_text)
        except Exception as e:
            send_message(chat_id, f"Gemini parsing failed: {e}")
            return jsonify({"ok": False}), 500

        send_message(chat_id, f"Parsed {len(questions_json)} questions. Generating HTML quiz...")

        html = build_html_from_questions(questions_json, title=filename)
        html_bytes = html.encode("utf-8")
        html_filename = filename.replace(".pdf", "") + "_quiz.html"

        send_document(chat_id, html_filename, html_bytes)
        send_message(chat_id, "Finished — check your HTML quiz! 👍")
        return jsonify({"ok": True})

    send_message(chat_id, "Please send a PDF document containing the quiz.")
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))