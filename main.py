"""
Telegram Bot to suggest a restaurant based on some questions and a predefined list.
"""

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from textwrap import dedent
import food as food
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 5000))

# Stages
START_ROUTES, END_ROUTES = range(2)

# Callback data
ONE, TWO, THREE = range(3)

# Instantiate class
ChosenFood = food.Food()
choices = []


async def help(update, context):
    await update.message.reply_html(
        dedent(
            """\
        I can help you decide where you should eat.

        You can control me by sending these commands:

        <b>Standard</b>
        /start - does nothing
        /help - help menu

        <b>Let's eat</b>
        /eat - helps you decide where to eat
        """
        )
    )


async def start(update, context):
    await update.message.reply_html("Hello.")


async def eat(update, context):

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton(
                food.q1_options[0], callback_data="0. " + food.q1_options[0]
            ),
            InlineKeyboardButton(
                food.q1_options[1], callback_data="0. " + food.q1_options[1]
            ),
        ],
        [
            InlineKeyboardButton(
                food.q1_options[2], callback_data="0. " + food.q1_options[2]
            ),
            InlineKeyboardButton(
                food.q1_options[3], callback_data="0. " + food.q1_options[3]
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(food.q1, reply_markup=reply_markup)
    return START_ROUTES


async def question_2(update, context):
    query = update.callback_query

    await query.answer()

    chosen_selection_without_q = food.save_answer(choices, query.data)

    # filter data
    ChosenFood.filter(
        food.q1_dict, option=chosen_selection_without_q, column=None, single_col=False
    )

    keyboard = [
        [
            InlineKeyboardButton(
                food.q2_options[0], callback_data="1. " + food.q2_options[0]
            ),
            InlineKeyboardButton(
                food.q2_options[1], callback_data="1. " + food.q2_options[1]
            ),
            InlineKeyboardButton(
                food.q2_options[2], callback_data="1. " + food.q2_options[2]
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=food.q2, reply_markup=reply_markup)

    return START_ROUTES


async def question_3(update, context):
    query = update.callback_query
    await query.answer()

    chosen_selection_without_q = food.save_answer(choices, query.data)

    # filter data
    ChosenFood.filter(
        food.q2_dict,
        option=chosen_selection_without_q,
        column=food.q2_col,
        single_col=True,
    )

    keyboard = [
        [
            InlineKeyboardButton(
                food.q3_options[0], callback_data="0. " + food.q3_options[0]
            ),
            InlineKeyboardButton(
                food.q3_options[1], callback_data="0. " + food.q3_options[1]
            ),
            InlineKeyboardButton(
                food.q3_options[2], callback_data="0. " + food.q3_options[2]
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=food.q3, reply_markup=reply_markup)

    return END_ROUTES


async def end(update, context):

    query = update.callback_query
    await query.answer()

    chosen_selection_without_q = food.save_answer(choices, query.data)

    # filter data
    ChosenFood.filter(
        food.q3_dict,
        option=chosen_selection_without_q,
        column=food.q3_col,
        single_col=True,
    )

    # selected food
    ChosenFood.choose_food()

    text = dedent(f"""
        You chose {choices[0]}, {choices[1]} and {choices[2]}. 
        
        You should eat at <b>{ChosenFood.chosen_restaurant}</b>, {ChosenFood.chosen_location}.
    """)

    await query.edit_message_html(text=text)
    return ConversationHandler.END


def main():

    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("eat", eat)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(question_2, pattern="^" + str(ONE)),
                CallbackQueryHandler(question_3, pattern="^" + str(TWO)),
            ],
            END_ROUTES: [CallbackQueryHandler(end, pattern="^" + str(ONE))],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # use application.run_polling() instead of run_webhook() to test locally
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url="https://aoshen-telegram-bot.herokuapp.com/" + TOKEN,
    )


if __name__ == "__main__":
    main()
