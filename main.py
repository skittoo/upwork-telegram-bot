import telebot
import schedule
import time
import threading
from dotenv import load_dotenv
import os
from helper_functions import validate_rss_link, update_rss_links, convert_dict_to_message


load_dotenv()

bot = telebot.TeleBot(f"{os.environ['BOT_TOKEN']}")

chat_ids = [] # A list of chat ids to send messages for.
rss_urls = {} # Dictionary for saving all rss links and it's latest 10 job posts.

def job():
    """Scheduled job for getting all RSS links updates."""
    global chat_ids
    global rss_urls
    if rss_urls:
        printable_rss_urls, rss_urls = update_rss_links(rss_urls)
    else:
        return   

    for rss_url in printable_rss_urls:
        for job_post in printable_rss_urls[rss_url]:
            if chat_ids:
                for chat_id in chat_ids:
                    message = convert_dict_to_message(job_post)
                    bot.send_message(chat_id, message)
            

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
    global rss_urls
    if not validate_rss_link(message.text):
        bot.reply_to(message, "Invalid RSS link, please try again. see: https://github.com/skittoo/upwork-telegram-bot")
    else:
        if message.text in list(rss_urls.keys()):
            bot.reply_to(message, "RSS already saved.")
        else:
            rss_urls[message.text] = [] # Make an empty list of the job posts.
            bot.reply_to(message, "Got your RSS url.")

                        
# Scheduling a task for checking rss links.                       
schedule.every(int(os.environ['TIME_INTERVAL'])).seconds.do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

bot.polling(none_stop=True)
