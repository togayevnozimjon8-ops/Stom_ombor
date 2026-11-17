from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

TOKEN = "BU_YERGA_YANGI_TOKENINGNI_QOY"
OMBOR_ID = 8545196229

DATA = {"bemorlar": [], "bux": [], "tolovlar": []}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🦷 Stom Ombor ishga tushdi!\n\nEndi hamma ma'lumot senga saqlanadi.\n\nBuyruqlar:\n/hisobot - Hisobot")

async def webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = json.loads(update.message.web_app_data.data)
        global DATA
        DATA = data
        await context.bot.send_message(chat_id=OMBOR_ID, text="OMBOR_DATA:" + json.dumps(DATA))
        await update.message.reply_text("✅ Saqlandi!")
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")

async def hisobot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bemor = len(DATA["bemorlar"])
    kirim = sum([b["summa"] for b in DATA["bux"] if b["tur"]=="kirim"])
    chiqim = sum([b["summa"] for b in DATA["bux"] if b["tur"]=="chiqim"])
    tolov = sum(DATA["tolovlar"])
    await update.message.reply_text(f"📊 Hisobot\n\nBemorlar: {bemor} ta\nKirim: {kirim:,} so'm\nChiqim: {chiqim:,} so'm\nSof foyda: {kirim-chiqim:,} so'm\nInvestorga to'langan: {tolov:,}\nQoldi: {13000000-tolov:,}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hisobot", hisobot))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data))
app.run_polling()
