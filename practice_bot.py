from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
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
    # update.message.reply_text("Hello. 👋")
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            telegram.InlineKeyboardButton("Option 1", callback_data="1"),
            telegram.InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [telegram.InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Please choose:", reply_markup=reply_markup)

def button(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")

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

class Food:

    def __init__(self, data=pd.read_csv("./data/food.csv")):
        self.data = data
    
    def filter_food(self, option):
        
        data = self.data.copy()

        col = q1_dict[option]

        data = data[data[col]==1]
        
        self.data = data

        print(self.data)

    def choose_food(self):
        self.chosen_restaurant = self.data['restaurant'].iloc[0]
        self.chosen_location = self.data['location'].iloc[0]


q1_meal = "What meal is this for?"
q1_options = [["Breakfast 🥐", "Lunch 🍗"], ["Dinner 🍱", "Dessert 🍨"]]
q1_dict = {
    "Breakfast 🥐": "is_for_breakfast",
    "Lunch 🍗": "is_for_lunch",
    "Dinner 🍱": "is_for_dinner",
    "Dessert 🍨": "is_for_desert"
}

# Instantiate class
getFood = Food()

def eat(update, context):
    
    # Question 1
    reply_markup = telegram.ReplyKeyboardMarkup(q1_options, one_time_keyboard=True)
    update.message.reply_text(text=q1_meal, reply_markup=reply_markup)
    

def msg_handler(update, context):
    update.message.reply_text(f"You chose {update.message.text}")

    getFood.filter_food(update.message.text)
    getFood.choose_food()

    update.message.reply_text(f"You should go to {getFood.chosen_restaurant} at {getFood.chosen_location}")


def main():

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler("eat", eat))

    disp.add_handler(MessageHandler(Filters.text, msg_handler))
    disp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()



if __name__ == "__main__":
    main()
