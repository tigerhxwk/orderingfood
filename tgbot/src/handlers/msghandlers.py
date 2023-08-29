from aiogram import types, Dispatcher
from init_bot import foodBot, foodBotDispatcher, logger

TIME_LIMIT_STRING = "Совместные заказы принимаются до 10:30 утра."

async def starter (message):
    logger.debug(f"user {message.chat.username} {message.chat.first_name} {message.chat.last_name} used starter")
    buttons = types.InlineKeyboardMarkup ()
    menu_btn = types.InlineKeyboardButton("Меню", callback_data="menu")
    cart_btn = types.InlineKeyboardButton("Корзина 🛒", callback_data="show_cart")
    end_btn = types.InlineKeyboardButton("Передумал(а) ✋", callback_data="discard")
    buttons.row(menu_btn, cart_btn)
    buttons.row(end_btn)
    await foodBot.sendMessage(message, 'Что делаем?', markup=buttons, clear=True)

async def greeter (message):
    await foodBot.sendMessage(message, f"Привет, {message.chat.username}! \n" + TIME_LIMIT_STRING)
    await starter(message)

def register_message_handlers (foodBotDispatcher : Dispatcher):
    foodBotDispatcher.register_message_handler(greeter, commands='start')
