import telebot
import schedule
import time
import threading
from dotenv import load_dotenv
import os
from helper_functions import validate_rss_link


load_dotenv()

bot = telebot.TeleBot(f"{os.environ['BOT_TOKEN']}")

chat_ids = [] # A list of chat ids to send messages for.
rss_links = {} # Dictionary for saving all rss links and it's latest 10 job posts.

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
def check_rss(message):
    global rss_links
    if validate_rss_link(message.text):
        bot.reply_to(message, "Invalid RSS link, please try again. see: https://github.com/skittoo/upwork-telegram-bot")
    else:
        if message.text in list(rss_links.keys()):
            bot.reply_to(message, "RSS already saved.")
        else:
            rss_links[message.text] = [] # Make an empty list of the job posts.
                        
# Scheduling a task for checking rss links.                       
schedule.every(os.environ['TIME_INTERVAL']).seconds.do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

bot.polling(none_stop=True)
