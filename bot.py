from flask import Flask
from threading import Thread
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot ishlayapti!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
Thread(target=run_flask, daemon=True).start()

# Oddiy xotira - hozircha shu yerda saqlanadi
DB = {"bemorlar": [], "kirim": 0, "chiqim": 0, "texniklar": ["Aziz - Keramika", "Jasur - Protez"]}

def bosh_menu():
    kb = [
        [InlineKeyboardButton("👥 Bemorlar", callback_data="bemorlar")],
        [InlineKeyboardButton("💰 Buxgalteriya", callback_data="bux")],
        [InlineKeyboardButton("🧮 Kalkulyator", callback_data="kalk")],
        [InlineKeyboardButton("🛠 Texniklar", callback_data="texnik")],
        [InlineKeyboardButton("📊 Hisobot", callback_data="hisobot")],
    ]
    return InlineKeyboardMarkup(kb)

def ortga():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🦷 STOM BUXGALTERIYA ga xush kelibsiz!\n\nKerakli bo'limni tanlang:",
        reply_markup=bosh_menu()
    )

async def tugma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d == "home":
        context.user_data.clear()
        await q.edit_message_text("🦷 Bosh sahifa:\n\nKerakli bo'limni tanlang:", reply_markup=bosh_menu())

    elif d == "bemorlar":
        kb = [
            [InlineKeyboardButton("➕ Bemor qo'shish", callback_data="bemor_add")],
            [InlineKeyboardButton("📋 Bemorlar ro'yxati", callback_data="bemor_list")],
            [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]
        ]
        await q.edit_message_text("👥 Bemorlar bo'limi:", reply_markup=InlineKeyboardMarkup(kb))

    elif d == "bemor_add":
        context.user_data["holat"] = "bemor_add"
        await q.edit_message_text("Bemor ismi va ishini yozing.\nMisol: Ali - Implant\n\nBekor qilish uchun /start bosing", reply_markup=ortga())

    elif d == "bemor_list":
        if not DB["bemorlar"]:
            txt = "Hozircha bemor yo'q."
        else:
            txt = "📋 Bemorlar:\n\n" + "\n".join([f"{i+1}. {b}" for i, b in enumerate(DB["bemorlar"])])
        await q.edit_message_text(txt, reply_markup=ortga())

    elif d == "bux":
        kb = [
            [InlineKeyboardButton("➕ Kirim qo'shish", callback_data="kirim")],
            [InlineKeyboardButton("➖ Chiqim qo'shish", callback_data="chiqim")],
            [InlineKeyboardButton("💰 Balans", callback_data="balans")],
            [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]
        ]
        await q.edit_message_text("💰 Buxgalteriya:", reply_markup=InlineKeyboardMarkup(kb))

    elif d == "kirim":
        context.user_data["holat"] = "kirim"
        await q.edit_message_text("Kirim summasini yozing.\nMisol: 500000", reply_markup=ortga())
    elif d == "chiqim":
        context.user_data["holat"] = "chiqim"
        await q.edit_message_text("Chiqim summasini yozing.\nMisol: 200000", reply_markup=ortga())
    elif d == "balans":
        bal = DB["kirim"] - DB["chiqim"]
        await q.edit_message_text(f"💰 Balans:\n\nKirim: {DB['kirim']:,} so'm\nChiqim: {DB['chiqim']:,} so'm\nQoldiq: {bal:,} so'm", reply_markup=ortga())

    elif d == "kalk":
        kb = [
            [InlineKeyboardButton("🦷 Implant: 3 500 000", callback_data="k_3500000")],
            [InlineKeyboardButton("🦷 Vinir: 1 200 000", callback_data="k_1200000")],
            [InlineKeyboardButton("🦷 Plomba: 400 000", callback_data="k_400000")],
            [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]
        ]
        await q.edit_message_text("🧮 Kalkulyator - ishni tanlang, narxni hisoblayman:", reply_markup=InlineKeyboardMarkup(kb))

    elif d.startswith("k_"):
        narx = int(d.split("_")[1])
        texnik = int(narx * 0.30)
        klinika = narx - texnik
        await q.edit_message_text(f"🧮 Hisob:\n\nIsh narxi: {narx:,} so'm\nTexnikka (30%): {texnik:,} so'm\nKlinikaga: {klinika:,} so'm", reply_markup=ortga())

    elif d == "texnik":
        txt = "🛠 Texniklar:\n\n" + "\n".join([f"{i+1}. {t}" for i, t in enumerate(DB["texniklar"])])
        kb = [
            [InlineKeyboardButton("➕ Texnik qo'shish", callback_data="texnik_add")],
            [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")]
        ]
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))

    elif d == "texnik_add":
        context.user_data["holat"] = "texnik_add"
        await q.edit_message_text("Texnik ismi va ishini yozing.\nMisol: Sardor - Sirkon", reply_markup=ortga())

    elif d == "hisobot":
        bal = DB["kirim"] - DB["chiqim"]
        txt = f"📊 HISOBOT\n\n👥 Bemorlar: {len(DB['bemorlar'])} ta\n💰 Kirim: {DB['kirim']:,} so'm\n➖ Chiqim: {DB['chiqim']:,} so'm\n✅ Qoldiq: {bal:,} so'm\n🛠 Texniklar: {len(DB['texniklar'])} ta"
        await q.edit_message_text(txt, reply_markup=ortga())

async def matn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    holat = context.user_data.get("holat")
    txt = update.message.text
    if not holat:
        await update.message.reply_text("Bosh sahifaga qaytish uchun /start bosing")
        return
    if holat == "bemor_add":
        DB["bemorlar"].append(txt)
        await update.message.reply_text(f"✅ Bemor qo'shildi: {txt}", reply_markup=bosh_menu())
    elif holat == "texnik_add":
        DB["texniklar"].append(txt)
        await update.message.reply_text(f"✅ Texnik qo'shildi: {txt}", reply_markup=bosh_menu())
    elif holat == "kirim":
        try:
            DB["kirim"] += int(txt.replace(" ", ""))
            await update.message.reply_text("✅ Kirim qo'shildi!", reply_markup=bosh_menu())
        except:
            await update.message.reply_text("Faqat raqam yozing! Misol: 500000")
            return
    elif holat == "chiqim":
        try:
            DB["chiqim"] += int(txt.replace(" ", ""))
            await update.message.reply_text("✅ Chiqim qo'shildi!", reply_markup=bosh_menu())
        except:
            await update.message.reply_text("Faqat raqam yozing! Misol: 200000")
            return
    context.user_data.clear()

def main():
    token = os.environ.get("BOT_TOKEN")
    ilova = Application.builder().token(token).build()
    ilova.add_handler(CommandHandler("start", start))
    ilova.add_handler(CallbackQueryHandler(tugma))
    ilova.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, matn))
    ilova.run_polling()

if __name__ == "__main__":
    main()
