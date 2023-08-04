import json
from init_bot import logger

def make_menu (filepath):
    try:
        with open(filepath) as file:
            parsedMenu = json.load (file)
            logger.debug ("successfully opened menu file")
            for i in parsedMenu["category"]:
                logger.debug ("received categories:")
                logger.debug (f"\t{i}")
    except FileNotFoundError:
        logger.debug ("menu file does not exist")

    return parsedMenu
