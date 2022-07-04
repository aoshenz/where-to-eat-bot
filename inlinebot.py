from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import logging
from textwrap import dedent

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


with open("secret/keys.txt", "r") as f:
    TOKEN = f.read()


async def help(update, context):
    await update.message.reply_html(dedent("""\
        I can help you decide where you should eat.

        You can control me by sending these commands:

        <b>Standard</b>
        /start - does nothing
        /help - help menu

        <b>Let's eat</b>
        /eat - helps you decide where to eat
        """)
    )

# Stages
START_ROUTES, END_ROUTES = range(2)

# Callback data
ONE, TWO, THREE = range(3)

async def eat(update, context):

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("Breakfast", callback_data=str(ONE)),
            InlineKeyboardButton("Lunch", callback_data=str(ONE))
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option", reply_markup=reply_markup)

    return START_ROUTES

async def meal_type(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Hot", callback_data=str(TWO)),
            InlineKeyboardButton("Cold", callback_data=str(TWO))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Now choose between:", reply_markup=reply_markup
    )

    return START_ROUTES
    
async def another_q(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data=str(ONE)),
            InlineKeyboardButton("No", callback_data=str(ONE))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Last question:", reply_markup=reply_markup
    )

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
                CallbackQueryHandler(meal_type, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(another_q, pattern="^" + str(TWO) + "$")
            ],
            END_ROUTES: [
                CallbackQueryHandler(end, pattern="^" + str(ONE) + "$")
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help))

    application.run_polling()

if __name__ == "__main__":
    main()

