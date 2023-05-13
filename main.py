import telebot
import schedule
import time
import threading
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(f"{os.environ['BOT_TOKEN']}")

chat_ids = []

def job():
    """Scheduled job for getting all RSS links updates."""
    global chat_ids
    if chat_ids:
        for chat_id in chat_ids:
            bot.send_message(chat_id, "Message")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_ids
    new_chat_id = message.chat.id
    if new_chat_id not in chat_ids:
        chat_ids.append(new_chat_id)
    bot.reply_to(message, "Welcome, please enter your RSS link(s).")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Please follow the instructions in: https://github.com/skittoo/upwork-telegram-bot")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

schedule.every(5).seconds.do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

bot.polling(none_stop=True)
