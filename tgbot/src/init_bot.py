from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import logging, os

API_KEY_FILE = os.getcwd() + "/tgbot/http_api.key"

try:
    keyfile = open(API_KEY_FILE, "r")
except FileNotFoundError:
    logger.debug ("file does not exist")
    os.exit(1)

foodBot = Bot(keyfile.read().replace('\n', ''))
foodBotDispatcher = Dispatcher(foodBot)

logger = logging.getLogger("actionlogger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
