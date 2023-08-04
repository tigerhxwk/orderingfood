import json
from init_bot import logger

def make_menu (filepath):
    try:
        with open(filepath) as file:
            parsedMenu = json.load (file)
            logger.debug ("successfully opened menu file")

    except FileNotFoundError:
        logger.debug ("menu file does not exist")
        return 1

    for category in parsedMenu.keys():
        logger.debug ("received categories:")
        logger.debug (f"\t{category}")

    return parsedMenu
