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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

with open("secret/keys.txt", "r") as f:
    TOKEN = f.read()

# Stages
START_ROUTES, END_ROUTES = range(2)

# Callback data
ONE, TWO, THREE = range(3)

# Instantiate class
ChosenFood = food.Food()


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


async def eat(update, context):

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton(food.q1_options[0], callback_data="0. lol"),
            InlineKeyboardButton(food.q1_options[1], callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(food.q1_options[2], callback_data=str(ONE)),
            InlineKeyboardButton(food.q1_options[3], callback_data=str(ONE)),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(food.q1, reply_markup=reply_markup)
    return START_ROUTES


async def meal_type(update, context):
    query = update.callback_query

    await query.answer()
    logger.info(query.data)

    keyboard = [
        [
            InlineKeyboardButton(food.q2_options[0], callback_data=str(TWO)),
            InlineKeyboardButton(food.q2_options[1], callback_data=str(TWO)),
            InlineKeyboardButton(food.q2_options[2], callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=food.q2, reply_markup=reply_markup)

    return START_ROUTES


async def cost(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data=str(ONE)),
            InlineKeyboardButton("No", callback_data=str(ONE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Last question:", reply_markup=reply_markup)

    return END_ROUTES


def start(update, context):
    update.message.reply("Hello.")


async def end(update, context):

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="You should eat: ")
    return ConversationHandler.END


def main():

    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("eat", eat)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(meal_type, pattern="^" + str(ONE)),
                CallbackQueryHandler(cost, pattern="^" + str(TWO) + "$"),
            ],
            END_ROUTES: [CallbackQueryHandler(end, pattern="^" + str(ONE) + "$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help))

    application.run_polling()


if __name__ == "__main__":
    main()
