import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Токен из переменных окружения

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Бот запущен на Railway!")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    
    print("✅ Бот запущен и работает...")
    updater.start_polling()
    updater.idle()  # Блокирует поток, пока бот активен

if __name__ == "__main__":
    main()
