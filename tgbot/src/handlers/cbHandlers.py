from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from init_bot import foodBot, foodBotDispatcher, logger
from handlers.msghandlers import starter as starter
from menu import buttons_builder

categoryButtons = None
parsedMenu = None
async def category_callback (callback :types.CallbackQuery):
    logger.debug (f"{category_callback.__name__} received {callback.data}")
#     this callback handles callback data that begins with category_<id>
#     idea is to take id and us it in parsed menu to get according list of dishes


async def menu_printer(callback :types.CallbackQuery):
    global categoryButtons
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}\
                {callback.message.chat.last_name} selected menu")

    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")

    await foodBot.send_message(callback.message.chat.id, "Выбирай категорию:", reply_markup=categoryButtons)

async def discard (callback : types.CallbackQuery):
    #need to make cart and 'end' features
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}\
                {callback.message.chat.last_name} changed his mind")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")

    await foodBot.send_message(callback.message.chat.id, "Будем ждать снова!")
    await starter(callback.message)

async def show_cart (callback : types.CallbackQuery):
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}\
                {callback.message.chat.last_name} requested cart")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    await foodBot.send_message(callback.message.chat.id, "Корзина по техническим причинам недоступна")
    await starter(callback.message)

async def nothing_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Ждем тебя снова!")
    await menu_printer(callback)

def register_callbacks_handler (foodDispatcher : Dispatcher, Menu : dict ()):
    global categoryButtons, parsedMenu
    parsedMenu = Menu
    foodDispatcher.register_callback_query_handler(menu_printer, Text(equals="menu"))
    foodDispatcher.register_callback_query_handler(discard, Text(equals="discard"))
    foodDispatcher.register_callback_query_handler(show_cart, Text(equals="show_cart"))
    foodDispatcher.register_callback_query_handler(category_callback, Text(startswith="category_"))
    categoryButtons = buttons_builder.create_categories_buttons(parsedMenu)
    logger.debug ("registered callbacks and created buttons")
