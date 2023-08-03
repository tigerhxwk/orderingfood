#!/usr/bin/python3

from aiogram.utils import executor
from init_bot import foodBotDispatcher, logger
from datetime import datetime
from handlers import msghandlers
from handlers import cbHandlers
from menu import menu_builder
import os, json

TIME_LIMIT_STRING = "Совместные заказы принимаются до 11:30 утра."

PARSED_MENU_JSON_FILE = os.getcwd() + "/data.json"

async def on_startup (_):
    logger.debug("Bot started successfully")

async def on_shutdown (_):
    logger.debug("Bot is going down")

def main ():
    msghandlers.register_message_handlers(foodBotDispatcher)
    parsedMenu = menu_builder.make_menu(PARSED_MENU_JSON_FILE)

    cbHandlers.register_callbacks_handler(foodBotDispatcher, parsedMenu)

    executor.start_polling(foodBotDispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
	main()
