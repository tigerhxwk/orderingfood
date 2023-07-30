from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from init_bot import foodBot, foodBotDispatcher, logger
from handlers.msghandlers import starter as starter

async def menu_printer(callback :types.CallbackQuery):
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}\
                {callback.message.chat.last_name} selected menu")
    keyboard = [
        [
            types.InlineKeyboardButton("Бизнес-ланчи", callback_data="business_lunch"),
            types.InlineKeyboardButton("Холодные блюда", callback_data="cold_meal"),
        ],
        [
            types.InlineKeyboardButton("Супы", callback_data="soups"),
            types.InlineKeyboardButton("Вторые блюда", callback_data="second_meal"),
        ],
        [
            types.InlineKeyboardButton("Гарниры", callback_data="garnish"),
            types.InlineKeyboardButton("Напитки", callback_data="beverages"),
        ],
        [
            types.InlineKeyboardButton("Суши, роллы, вок, паста", callback_data="asian"),
            types.InlineKeyboardButton("Выпечка", callback_data="bakery"),
        ],
        [
            types.InlineKeyboardButton("Торт", callback_data="cake"),
            types.InlineKeyboardButton("Пицца", callback_data="pizza"),
            types.InlineKeyboardButton("Завтрак", callback_data="breakfast"),
        ],
        [
            types.InlineKeyboardButton("Хлеб, соусы, добавки", callback_data="bread"),
            types.InlineKeyboardButton("Блины, сырники, вареники", callback_data="pancakes"),
        ],
        [types.InlineKeyboardButton("Ничего", callback_data="nothing")]
    ]

    reply_btns = types.InlineKeyboardMarkup(row_width=2)
    # goddam 'list in list' iterator
    for i in keyboard:
        for j in i:
            reply_btns.insert(j)
        reply_btns.row()
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")

    await foodBot.send_message(callback.message.chat.id, "Выбирай категорию:", reply_markup=reply_btns)

# @foodBotDispatcher.message_handler (startswith = ['Передумал(а)'])
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

# @foodBotDispatcher.message_handler (startswith = ['Корзина'])
async def show_cart (callback : types.CallbackQuery):
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}\
                {callback.message.chat.last_name} requested cart")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    await foodBot.send_message(callback.message.chat.id, "Корзина по техническим причинам недоступна")
    await starter(callback.message)

async def business_lunch_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по бизнес-ланчам нет 😔")
    await menu_printer(callback)

async def cold_meal_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по первым блюдам нет 😔")
    await menu_printer(callback)

async def soups_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по супам нет 😔")
    await menu_printer(callback)

async def second_meal_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по вторым блюдам нет 😔")
    await menu_printer(callback)

async def garnish_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по гарнирам нет 😔")
    await menu_printer(callback)

async def beverages_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по напиткам нет 😔")
    await menu_printer(callback)

async def asian_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по азиатской кухне нет 😔")
    await menu_printer(callback)

async def bakery_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по выпечке нет 😔")
    await menu_printer(callback)

async def cake_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по тортам нет 😔")
    await menu_printer(callback)

async def pizza_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по пицце нет 😔")
    await menu_printer(callback)

async def breakfast_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по завтракам нет 😔")
    await menu_printer(callback)

async def bread_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по хлебу нет 😔")
    await menu_printer(callback)

async def pancakes_handler (callback : types.CallbackQuery):
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")
    try:
        await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id - 1}")
    await foodBot.send_message(callback.message.chat.id, "Информации по блинчикам нет 😔")
    await menu_printer(callback)

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

callback_map = {
    'business_lunch':business_lunch_handler,
    'cold_meal':cold_meal_handler,
    'soups':soups_handler,
    'second_meal':second_meal_handler,
    'garnish':garnish_handler,
    'beverages':beverages_handler,
    'asian':asian_handler,
    'bakery':bakery_handler,
    'cake':cake_handler,
    'pizza':pizza_handler,
    'breakfast':breakfast_handler,
    'bread':bread_handler,
    'pancakes':pancakes_handler,
    'nothing':nothing_handler
}

def register_callbacks_handler (foodDispatcher : Dispatcher):
    foodDispatcher.register_callback_query_handler(menu_printer, Text(equals="menu"))
    foodDispatcher.register_callback_query_handler(discard, Text(equals="discard"))
    foodDispatcher.register_callback_query_handler(show_cart, Text(equals="show_cart"))
    for cBack in callback_map:
        logger.debug (f"registering text: {cBack} as {callback_map[cBack]}")
        foodDispatcher.register_callback_query_handler(callback_map[cBack], Text(equals=cBack))
