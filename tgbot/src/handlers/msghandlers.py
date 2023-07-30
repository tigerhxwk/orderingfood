from aiogram import types, Dispatcher
from init_bot import foodBot, foodBotDispatcher, logger

TIME_LIMIT_STRING = "Совместные заказы принимаются до 11:30 утра."

# @foodBotDispatcher.message_handler (commands = ['start'])
async def starter (message):
    logger.debug(f"user {message.chat.username} {message.chat.first_name} {message.chat.last_name} used starter")
    buttons = types.InlineKeyboardMarkup ()
    menu_btn = types.InlineKeyboardButton("Меню", callback_data="menu")
    cart_btn = types.InlineKeyboardButton("Корзина 🛒", callback_data="show_cart")
    end_btn = types.InlineKeyboardButton("Передумал(а) ✋", callback_data="discard")
    buttons.row(menu_btn, cart_btn)
    buttons.row(end_btn)
    await foodBot.send_message(message.chat.id, 'Что делаем?', reply_markup=buttons)

async def greeter (message):
    await foodBot.send_message(message.chat.id, f"Привет, {message.chat.username}! \n" + TIME_LIMIT_STRING)
    await starter(message)

def register_message_handlers (foodBotDispathcer : Dispatcher):
    foodBotDispathcer.register_message_handler(greeter, commands='start')
