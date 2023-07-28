#!/usr/bin/python3.9.6
import telebot
from telebot import types
import logging
from datetime import datetime

api_file = open ("../http_api.key", "r")
api_token = api_file.read().replace('\n', '')

foodBot = telebot.TeleBot(api_token)

TIME_LIMIT_STRING = "Совместные заказы принимаются до 11:30 утра."

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger("actionlogger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def business_lunch_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по бизнес-ланчам нет 😔")
    menu_printer(callback.message)

def cold_meal_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по первым блюдам нет 😔")
    menu_printer(callback.message)

def soups_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по супам нет 😔")
    menu_printer(callback.message)

def second_meal_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по вторым блюдам нет 😔")
    menu_printer(callback.message)

def garnish_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по гарнирам нет 😔")
    menu_printer(callback.message)

def beverages_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по напиткам нет 😔")
    menu_printer(callback.message)

def asian_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по азиатской кухне нет 😔")
    menu_printer(callback.message)

def bakery_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по выпечке нет 😔")
    menu_printer(callback.message)

def cake_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по тортам нет 😔")
    menu_printer(callback.message)

def pizza_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по пицце нет 😔")
    menu_printer(callback.message)

def breakfast_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по завтракам нет 😔")
    menu_printer(callback.message)

def bread_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по хлебу нет 😔")
    menu_printer(callback.message)

def pancakes_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Информации по блинчикам нет 😔")
    menu_printer(callback.message)

def nothing_handler (callback):
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id)
    foodBot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    foodBot.send_message(callback.message.chat.id, "Ждем тебя снова!")
    menu_printer(callback.message)


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

@foodBot.message_handler (commands = ['start'])
def starter (message):
    logger.debug(f"user {message.chat.username} {message.chat.first_name} {message.chat.last_name} used starter")
    buttons = types.ReplyKeyboardMarkup ()
    menu_btn = types.KeyboardButton("Меню 🍔")
    cart_btn = types.KeyboardButton("Корзина 🛒")
    end_btn = types.KeyboardButton("Я передумал(а) ✋")
    buttons.row(menu_btn)
    buttons.row(cart_btn, end_btn)
    foodBot.send_message(message.chat.id, f"Привет, {message.chat.username}! \n" + TIME_LIMIT_STRING, reply_markup=buttons)
    foodBot.register_next_step_handler(message, btn_click_handler)

def btn_click_handler(message):
    if 'меню' in message.text.lower ():
        logger.debug(f"user {message.chat.username} {message.chat.first_name} {message.chat.last_name} selected menu")
        menu_printer (message)
    elif 'корзина' in message.text.lower ():
        logger.debug(f"user {message.chat.username} {message.chat.first_name} {message.chat.last_name} selected cart")
        foodBot.send_message(message.chat.id, "Корзина в разработке...")
    elif 'передумал' in message.text.lower():
    #     need to make cart and 'end' features
        logger.debug(f"user {message.chat.username} {message.chat.first_name} {message.chat.last_name} changed his mind")
        foodBot.send_message(message.chat.id, "Приходи еще!")
    else:
        foodBot.send_message(message.chat.id, "Я такое не знаю, попробуй еще")
    # to do - make starter case here
    foodBot.register_next_step_handler(message, btn_click_handler)

def menu_printer(message):
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

    reply_btns = types.InlineKeyboardMarkup(keyboard)
    foodBot.send_message(message.chat.id, "Выбирай категорию:", reply_markup=reply_btns)


@foodBot.callback_query_handler(func=lambda callback:True)
def cbhandler (callback):
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}" +
                 f" {callback.message.chat.last_name} selected {callback.data}")
    callback_map[callback.data](callback)


foodBot.infinity_polling ()