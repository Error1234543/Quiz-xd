import telebot
import fitz  # PyMuPDF for PDF text extraction
import requests
import json

# -----------------------------
# CONFIG
# -----------------------------
BOT_TOKEN = "8343622832:AAEtx-oxmBImv_SLPAGF8Z42aPUXdzTGT9c"
GEMINI_API_KEY = "AIzaSyB5TA6nDIj8VARsC4LPfdxu7_HBnetmPg8"

bot = telebot.TeleBot(BOT_TOKEN)

# Allowed users list
authorized_users = set()

# -----------------------------
# GEMINI AI — DIRECT API (NO ENV Needed)
# -----------------------------
def gemini_extract_questions(pdf_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
    Extract MCQ questions from this Gujarati PDF text.
    Output JSON only in this format:
    [
        {{
            "question": "text",
            "options": ["A","B","C","D"],
            "answer": "correct option text"
        }}
    ]

    PDF TEXT:
    {pdf_text}
    """

    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    res = requests.post(url, json=body)
    data = res.json()

    try:
        output = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(output)
    except:
        return None


# -----------------------------
# PDF to TEXT
# -----------------------------
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# -----------------------------
# AUTH FUNCTIONS
# -----------------------------
def is_auth(uid):
    return uid in authorized_users

@bot.message_handler(commands=['adduser'])
def add_user(msg):
    if str(msg.from_user.id) != "7447651332":
        return bot.reply_to(msg, "❌ Only owner can add users.")

    try:
        uid = int(msg.text.split()[1])
        authorized_users.add(uid)
        bot.reply_to(msg, f"✅ User {uid} added.")
    except:
        bot.reply_to(msg, "⚠️ Usage: /adduser 123456789")

@bot.message_handler(commands=['removeuser'])
def remove_user(msg):
    if str(msg.from_user.id) != "7447651332":
        return bot.reply_to(msg, "❌ Only owner can remove users.")

    try:
        uid = int(msg.text.split()[1])
        authorized_users.discard(uid)
        bot.reply_to(msg, f"🗑️ User {uid} removed.")
    except:
        bot.reply_to(msg, "⚠️ Usage: /removeuser 123456789")


# -----------------------------
# START
# -----------------------------
@bot.message_handler(commands=['start'])
def start_msg(msg):
    bot.reply_to(msg, "👋 Welcome to Sonic Quiz Bot!\nSend /quiz to upload your PDF quiz.")


# -----------------------------
# QUIZ COMMAND
# -----------------------------
@bot.message_handler(commands=['quiz'])
def start_quiz(msg):
    if not is_auth(msg.from_user.id):
        return bot.reply_to(msg, "❌ You are not authorized.\nDM: t.me/xdsonic for premium access.")

    bot.reply_to(msg, "📄 Send your PDF file…")


# -----------------------------
# HANDLE PDF FILE
# -----------------------------
@bot.message_handler(content_types=['document'])
def handle_pdf(msg):
    if not is_auth(msg.from_user.id):
        return bot.reply_to(msg, "❌ You are not authorized.\nDM: t.me/xdsonic")

    file_info = bot.get_file(msg.document.file_id)
    downloaded = bot.download_file(file_info.file_path)

    pdf_path = "quiz.pdf"
    with open(pdf_path, "wb") as f:
        f.write(downloaded)

    bot.reply_to(msg, "🔍 Extracting text…")

    text = extract_text_from_pdf(pdf_path)
    bot.reply_to(msg, "🤖 Sending to Gemini AI…")

    questions = gemini_extract_questions(text)
    if not questions:
        return bot.reply_to(msg, "❌ Gemini parsing failed. Try again!")

    bot.reply_to(msg, f"✅ Total {len(questions)} questions found!\nSending quiz…")

    # -----------------------------
    # SEND QUIZ POLLS
    # -----------------------------
    for i, q in enumerate(questions, start=1):
        question = f"{i}) {q['question']}"
        options = q["options"]
        correct = options.index(q["answer"])

        bot.send_poll(
            msg.chat.id,
            question,
            options,
            type="quiz",
            correct_option_id=correct,
            is_anonymous=False
        )

    bot.send_message(msg.chat.id, "🎉 Quiz completed & sent!")


# -----------------------------
# RUN BOT
# -----------------------------
print("Bot Running…")
bot.infinity_polling()