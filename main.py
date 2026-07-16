import os
import requests
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- 24/7 SERVER SETUP ---
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is alive 24/7!"

def run_flask():
    # Cloud hosting ke liye port 8000 jaruri hai
    app_flask.run(host='0.0.0.0', port=8000)
# -------------------------

# Environment variables se token aur keys uthayein (Security ke liye)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "iW5UKo8wEfpqHg3Xw3i3" # Neil Voice ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Main ElevenLabs Neil voice bot hu. Main 24/7 active hu!")

async def convert_text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id
    filename = f"voice_{chat_id}.ogg"

    url = f"https://elevenlabs.io{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": user_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            with open(filename, 'rb') as voice_file:
                await context.bot.send_voice(chat_id=chat_id, voice=voice_file)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_text_to_voice))
    
    # Background me Flask server chalu karein jo bot ko sone nahi dega
    threading.Thread(target=run_flask).start()
    
    print("Bot 24/7 mode me chalu ho gaya hai...")
    app.run_polling()

if __name__ == '__main__':
    main()
