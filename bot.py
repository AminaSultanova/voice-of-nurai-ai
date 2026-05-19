import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from ai_assistant import ask_ai

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Voice of Nurai — AI Safety Assistant\n\n"
        "Я помогаю девушкам в опасных ситуациях.\n"
        "Опишите, что происходит, и я дам инструкцию.\n\n"
        "Примеры:\n"
        "- Я иду по темной улице, за мной кто-то идет\n"
        "- Подозрительное такси\n"
        "- Я потерялась в незнакомом районе\n\n"
        "Команды:\n"
        "/start — приветствие\n"
        "/sos — экстренная инструкция\n"
        "/help — что я умею"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Voice of Nurai — Что я умею:\n\n"
        "1. Задайте вопрос о безопасности — я дам совет.\n"
        "2. /sos — мгновенная экстренная инструкция.\n\n"
        "В критической ситуации: кнопка SOS в приложении Nurai или звонок 112."
    )


async def sos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ЭКСТРЕННАЯ ИНСТРУКЦИЯ:\n\n"
        "1. СОХРАНЯЙТЕ СПОКОЙСТВИЕ\n"
        "2. НАЖМИТЕ SOS-КНОПКУ в приложении Nurai\n"
        "3. ЗАЙДИТЕ в ближайший магазин, аптеку или кафе\n"
        "4. ЗВОНИТЕ 112\n"
        "5. ПЕРЕЙДИТЕ на освещенную сторону улицы\n"
        "6. ЖДИТЕ ПОМОЩЬ в безопасном месте"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    answer = ask_ai(user_message)

    if answer:
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, нажмите SOS-кнопку в приложении Nurai "
            "или позвоните 112."
        )


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("sos", sos_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()