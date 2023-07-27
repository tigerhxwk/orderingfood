import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ( ApplicationBuilder,
        ContextTypes,
        CommandHandler,
        filters,
        MessageHandler,
        CallbackQueryHandler,
        ConversationHandler
)

from datetime import datetime

WARNING_STRING = "Пока что тут все в разработке 🧑‍💻, придется подождать"
TIME_LIMIT_STRING = "Совместные заказы принимаются до 11:30 утра."
UNKNOWN_CMD_STRING = "Я такое не знаю 😐"

api_file = open ("../http_api.key", "r")
api_token = api_file.read().replace('\n', '')

updater = Update(api_token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger("actionlogger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query
    await query.answer()


    logger.debug (f"user selected {query.data}")
    await query.edit_message_text(text=WARNING_STRING)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    logger.debug (f"user {update.message.chat.username} requested menu")
    keyboard = [
        [
            InlineKeyboardButton("Бизнес-ланчи", callback_data="business_lunch"),
            InlineKeyboardButton("Холодные блюда", callback_data="cold_meal"),
        ],
        [
            InlineKeyboardButton("Супы", callback_data="soups"),
            InlineKeyboardButton("Вторые блюда", callback_data="second_meal"),
        ],
        [
            InlineKeyboardButton("Гарниры", callback_data="garnish"),
            InlineKeyboardButton("Напитки", callback_data="beverages"),
        ],
        [
            InlineKeyboardButton("Суши, роллы, вок, паста", callback_data="asian"),
            InlineKeyboardButton("Выпечка", callback_data="bakery"),
        ],
        [
            InlineKeyboardButton("Торт", callback_data="cake"),
            InlineKeyboardButton("Пицца", callback_data="pizza"),
            InlineKeyboardButton("Завтрак", callback_data="breakfast"),
        ],
        [
            InlineKeyboardButton("Хлеб, соусы, добавки", callback_data="bread"),
            InlineKeyboardButton("Блины, сырники, вареники", callback_data="pancakes"),
        ],
        [InlineKeyboardButton("Ничего", callback_data="nothing")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выбирай категорию:", reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.chat.username
    chatId = chat_id=update.effective_chat.id
    time = datetime.now()
    logger.debug (f"{time} user {username} started conversation")
    currentTime = time.strftime("%H:%M")
    await context.bot.send_message(chatId, text=(f"Привет, {username}!"))
    await context.bot.send_message(chatId, text=TIME_LIMIT_STRING + (" Сейчас %s\n" % currentTime) +  "Посмотришь /menu?")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=UNKNOWN_CMD_STRING)

if __name__ == '__main__':

    application = ApplicationBuilder().token(api_token).build()


    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    menu_handler = CommandHandler('menu', menu)
    application.add_handler(menu_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
