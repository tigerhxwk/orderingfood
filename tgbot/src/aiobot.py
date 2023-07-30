#!/usr/bin/python3.9.6

from aiogram.utils import executor
from init_bot import foodBotDispatcher, logger
from datetime import datetime
from handlers import msghandlers
from handlers import cbHandlers

TIME_LIMIT_STRING = "Совместные заказы принимаются до 11:30 утра."

async def on_startup (_):
    logger.debug("Bot started successfully")

async def on_shutdown (_):
    logger.debug("Bot is goind down")

msghandlers.register_message_handlers(foodBotDispatcher)
cbHandlers.register_callbacks_handler(foodBotDispatcher)

executor.start_polling(foodBotDispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)