from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import logging, os

API_KEY_FILE = os.getcwd() + "/tgbot/http_api.key"

logger = logging.getLogger("actionlogger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
    keyfile = open(API_KEY_FILE, "r")
except FileNotFoundError:
    logger.debug ("key file does not exist")
    # exit is a built-in function
    exit(1)

foodBot = Bot(keyfile.read().replace('\n', ''))
foodBotDispatcher = Dispatcher(foodBot)

