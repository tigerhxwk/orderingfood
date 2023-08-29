import logging, os, sys
from botApi.foodBotApi import FoodBot
from gsheets.gsHandler import gHandler

API_KEY_FILE = os.getcwd() + "/tgbot/http_api.key"

logger = logging.getLogger("actionlogger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler = logging.FileHandler(f"{__name__}.log", mode='w')
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
    keyfile = open(API_KEY_FILE, "r")
except FileNotFoundError:
    logger.debug ("key file does not exist")
    # exit is a built-in function
    exit(1)

foodBot = FoodBot (keyfile.read().replace('\n', ''), logger)
Bot, foodBotDispatcher = foodBot.GimmeTheBot()

SheetApi = gHandler (logger)

if Bot == 0:
    logger.debug(f"shutting down the bot due to initialization error")
    exit(1)

