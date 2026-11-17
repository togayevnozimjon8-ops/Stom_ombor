from flask import Flask
from threading import Thread
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_flask, daemon=True).start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Bot ishlayapti!")

def main():
    token = os.environ.get("BOT_TOKEN")
    ilova = Application.builder().token(token).build()
    ilova.add_handler(CommandHandler("start", start))
    ilova.run_polling()

if __name__ == "__main__":
    main()
