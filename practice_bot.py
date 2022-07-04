from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import pandas as pd
import logging
from textwrap import dedent

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

with open("secret/keys.txt", "r") as f:
    TOKEN = f.read()

food = pd.read_csv("./data/food.csv")

print(food)

updater = Updater(TOKEN)
disp = updater.dispatcher

def start(update, context):
    update.message.reply_text("Hello. 👋")


def help(update, context):
    update.message.reply_text(dedent("""\
    I can help you decide where you should eat.

    You can control me by sending these commands:

    <b>Standard</b>
    /start - does nothing
    /help - help menu

    <b>Let's eat</b>
    /eat - helps you decide where to eat
    """),
        parse_mode=telegram.ParseMode.HTML,
    )


def eat(update, context):

    custom_keyboard = [["Breakfast 🥐", "Lunch 🍗"], ["Dinner 🍱", "Dessert 🍨"]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    update.message.reply_text(text="What meal is this for?", reply_markup=reply_markup)


def msg_handler(update, context):
    remove = telegram.ReplyKeyboardRemove()
    update.message.reply_text(f"You said {update.message.text}", reply_markup=remove)


def main():

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler("eat", eat))

    disp.add_handler(MessageHandler(Filters.text, msg_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
