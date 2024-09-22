# bot.py

import os
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# BOT_TOKEN = os.getenv('BOT_TOKEN', 'your-telegram-bot-token')
BOT_TOKEN = '7887662113:AAH4eB61DIivFoXCYV3vivRk9-7iBDvjEKU'
WEBAPP_URL = "https://7887-109-120-133-103.ngrok-free.app/articles/open/76767a23-8c74-4fb0-bf32-5fb3a54bbb58/"  # Ссылка на ваше мини-приложение

async def start(update: Update, context: CallbackContext):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Open Mini App", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
    )
    await update.message.reply_text("Welcome to the bot! Click the button to open the Mini App.", reply_markup=keyboard)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
