import os
from flask import Flask, request
import telebot

# ⚠️ توکن مستقیم داخل کد
TOKEN = "8216995020:AAGvoljr486O-2PItdAH7Rvgo_a_SSgAX5c"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📋 منو"))
    markup.add(KeyboardButton("💰 قیمت ها"), KeyboardButton("📞 تماس"))
    return markup

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(
        message.chat.id,
        "سلام 👋\nبه ربات خوش اومدی.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text

    if text == "📋 منو":
        bot.send_message(message.chat.id, "از دکمه‌ها استفاده کن.", reply_markup=main_menu())

    elif text == "💰 قیمت ها":
        bot.send_message(message.chat.id, "لیست قیمت:\nشماره مجازی: 2$\nاکانت: 5$")

    elif text == "📞 تماس":
        bot.send_message(message.chat.id, "آیدی پشتیبانی:\n@yourid")

    else:
        bot.send_message(message.chat.id, "پیامت دریافت شد ✅")

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN)
    app.run(host="0.0.0.0", port=PORT)