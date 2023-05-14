# upwork-telegram-bot
Telegram bot for getting new job posts on Upwork utilizing Upwork's rss links.

## Creating Your Own Telegram Bot
1- In Telegram search, enter `BotFather`

2- You will find the channel, enter and make a new bot /newbot

![alt text](./images/botfather.png)

3- You will get a bot token for your own telegram bot.

## Configuring the Bot.

1- In the main directory of the repo, make `.env` file. 

2- Put the bot token in `.env` same format as `.env.example` file. see: [Example .env](./.env.example)

3- Also, put the time interval you want to check the RSS urls.

## Install Requirements

`pip3 install -r requirements.txt`

## Run

`python3 main.py`

## Getting RSS Url From Upwork
1- Open Upwork.com, go to Find Work.

2- Put your search keyword and press search.

3- Get your RSS url for this search keyword.

![alt text](./images/rss_upwork.png)

4- It will open another page with XML content, copy it's url.

![alt text](./images/rssurl.png)

## Chat with Your Own Bot

1- Now, open your telegram bot by searching it's name or through it's Telegram invite link.

2- Put your rss url as a message for the bot 

![alt text](./images/tg_bot.png)













