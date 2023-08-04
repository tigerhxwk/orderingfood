from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from init_bot import foodBot, foodBotDispatcher, logger
from handlers.msghandlers import starter as starter
from menu import buttons_builder

categoryButtons = None
parsedMenu = None

def argument_overloader (input):
    if isinstance(input, types.CallbackQuery):
        selector = input.message.chat
        message_id = input.message.message_id
    else:
        selector = input.chat
        message_id = input.message_id

    return selector.username, selector.first_name, selector.last_name, selector.id, message_id

async def category_callback (callback :types.CallbackQuery):
    global parsedMenu

    data = callback.data
    logger.debug (f"{category_callback.__name__} received {data}")
#     this callback handles callback data that begins with category_<id>
#     idea is to take id and us it in parsed menu to get according list of dishes
    
    indexes = parsedMenu[data[9:]]
    markup = types.InlineKeyboardMarkup(row_width=1)

    for key in indexes.keys():
        names = indexes[key]['name']

        for name in names:
            markup.insert(types.InlineKeyboardButton(name, callback_data="discard"))

    await foodBot.send_message(callback.message.chat.id, "Выбирай:", reply_markup=markup)

async def menu_printer(callback :types.CallbackQuery):
    global categoryButtons
    # Kinda function overload, callback_query_handler gives here CallbackQuery,
    # but message_handler gives here message, that is nested field of CallbackQuery
    username, first_name, last_name, chat_id, message_id = argument_overloader (callback)
    logger.debug(f"user {username} {first_name} {last_name} selected menu")

    try:
        await foodBot.delete_message(chat_id, message_id)
    except:
        logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")

    await foodBot.send_message(chat_id, "Выбирай категорию:", reply_markup=categoryButtons)

async def discard (callback : types.CallbackQuery):
    #need to make cart and 'end' features
    username, first_name, last_name, chat_id, message_id = argument_overloader(callback)
    logger.debug(f"user {username} {first_name} {last_name} changed his mind")
    try:
        await foodBot.delete_message(chat_id, message_id)
    except:
        logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")
    try:
        await foodBot.delete_message(chat_id, message_id - 1)
    except:
        logger.debug(f"Unable to delete message {message_id - 1} from chat {chat_id}")

    await foodBot.send_message(chat_id, "Будем ждать снова!")


async def show_cart (callback : types.CallbackQuery):
    username, first_name, last_name, chat_id, message_id = argument_overloader(callback)
    logger.debug(f"user {username} {first_name} {last_name} requested cart")
    try:
        await foodBot.delete_message(chat_id, message_id)
    except:
        logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")
    await foodBot.send_message(chat_id, "Корзина по техническим причинам недоступна")

    if isinstance(callback, types.CallbackQuery):
        await starter(callback.message)
    else:
        await starter(callback)

async def nothing_handler (callback : types.CallbackQuery):
    _, first_name, _, chat_id, message_id = argument_overloader(callback)
    try:
        await foodBot.delete_message(chat_id, message_id)
    except:
        logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")
    try:
        await foodBot.delete_message(chat_id, message_id - 1)
    except:
        logger.debug(f"Unable to delete message {message_id - 1} from chat {chat_id}")

    logger.debug(f"{first_name} selected nothing")

    await menu_printer(callback)

def register_callbacks_handler (foodDispatcher : Dispatcher, Menu : dict ()):
    global categoryButtons, parsedMenu
    parsedMenu = Menu
    foodDispatcher.register_callback_query_handler(menu_printer, Text(equals="menu"))
    foodDispatcher.register_callback_query_handler(nothing_handler, Text(equals="discard"))
    foodDispatcher.register_callback_query_handler(show_cart, Text(equals="show_cart"))
    foodDispatcher.register_callback_query_handler(category_callback, Text(startswith="category_"))
    categoryButtons = buttons_builder.create_categories_buttons(parsedMenu)
    foodDispatcher.register_message_handler(menu_printer, commands='show_menu')
    foodDispatcher.register_message_handler(discard, commands='discard')
    foodDispatcher.register_message_handler(show_cart, commands='show_cart')
    logger.debug ("registered callbacks and created buttons")
