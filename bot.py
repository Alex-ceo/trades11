import os
from telegram import Update, InputMediaAnimation
from telegram.ext import Updater, CommandHandler, CallbackContext
from PIL import Image, ImageDraw, ImageFont
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Анимация корзины (создаем простую GIF)
def create_cart_animation():
    frames = []
    for i in range(5):
        img = Image.new("RGB", (200, 200), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        draw = ImageDraw.Draw(img)
        draw.text((50, 80), "🛒 Корзина", font=ImageFont.load_default())
        frames.append(img)
    frames[0].save("cart.gif", save_all=True, append_images=frames[1:], duration=500, loop=0)

# Товары в магазине
ITEMS = {
    "apple": {"price": 50, "emoji": "🍎"},
    "laptop": {"price": 1000, "emoji": "💻"},
    "book": {"price": 150, "emoji": "📚"}
}

def start(update: Update, context: CallbackContext):
    create_cart_animation()
    with open("cart.gif", "rb") as gif:
        update.message.reply_animation(
            animation=gif,
            caption="Добро пожаловать в наш магазин! 🛍️\n\nКоманды:\n/items - Товары\n/buy <item> - Купить"
        )

def show_items(update: Update, context: CallbackContext):
    items_text = "\n".join([f"{data['emoji']} {name} - {data['price']}₽" for name, data in ITEMS.items()])
    update.message.reply_text(f"📋 Товары:\n\n{items_text}")

def buy_item(update: Update, context: CallbackContext):
    item_name = context.args[0] if context.args else None
    if item_name in ITEMS:
        update.message.reply_text(f"✅ Вы купили {ITEMS[item_name]['emoji']} {item_name} за {ITEMS[item_name]['price']}₽!")
    else:
        update.message.reply_text("❌ Товар не найден. Смотрите /items")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("items", show_items))
    dp.add_handler(CommandHandler("buy", buy_item))
    
    print("🛒 Бот-магазин запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
