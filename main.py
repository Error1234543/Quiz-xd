from flask import Flask, request
import telebot
import os

from ocr_utils import extract_text_from_image
from gemini_utils import ask_gemini

TOKEN = "8343622832:AAEtx-oxmBImv_SLPAGF8Z42aPUXdzTGT9c"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# -----------------------------
# 🔥 WEBHOOK ROUTE (MUST MATCH EXACTLY)
# -----------------------------
@server.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    json_data = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# Simple alive check
@server.route("/")
def home():
    return "Bot Running Successfully 🔥"

# -----------------------------
# COMMAND HANDLERS
# -----------------------------

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🔥 Webhook Bot Working!\n📸 Send me an image and I will extract text using OCR.")

@bot.message_handler(commands=['ask'])
def ask_ai(msg):
    q = msg.text.replace("/ask", "").strip()
    if not q:
        bot.reply_to(msg, "❗ /ask <question>")
        return

    ans = ask_gemini(q)
    bot.reply_to(msg, ans)

# -----------------------------
# IMAGE OCR
# -----------------------------
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_data = bot.download_file(file_info.file_path)

    text = extract_text_from_image(file_data)
    bot.reply_to(message, f"📝 *Extracted OCR Text:*\n\n{text}", parse_mode="Markdown")

# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)