# bot.py
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)


from telegram import Update

import requests
from bs4 import BeautifulSoup

API_TOKEN = "" 

# what your bot should reply when we send the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome")
    update.message.reply_text("/topscorers: Top 10 Premier League Scorers")

def topscorers(update: Update, context: CallbackContext, ):
    url  = "https://www.goal.com/en/news/premier-league-top-scorers-2020-21/1qhjpasnphotl1lyikjfv6whva"

    main_list_scorers = []

    page = requests.get(url)
    page_content = page.content

    soup = BeautifulSoup(page_content, 'html.parser')
    information = soup.find_all("table", {"class": "tableizer-table"})
    for info in information:
        text = info.get_text()
        list_of_scorers = text.split("  ")
        for top_scorers in list_of_scorers[1:-1]:
            main_list_scorers.append(top_scorers)

    for scorers in main_list_scorers[:11]:
        update.message.reply_text(scorers)       


# the main function, with some boilerplate
def main():
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start)) # this line is what matters most
    dispatcher.add_handler(CommandHandler("topscorers", topscorers))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
