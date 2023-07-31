from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import logging

api_file = open ("../http_api.key", "r")
api_token = api_file.read().replace('\n', '')

foodBot = Bot(api_token)
foodBotDispatcher = Dispatcher(foodBot)

logger = logging.getLogger("actionlogger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
