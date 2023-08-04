from aiogram import types
from init_bot import logger

def create_categories_buttons (Menu : dict ()):
    categories = Menu.keys()

    menuCategories = []
    for category in categories:
        menuCategories.append(types.InlineKeyboardButton(category,
                                                          callback_data=f"category_{category}"))
        logger.debug (f"created menu button {category} and callback category_{category}")

    menuButtons = types.InlineKeyboardMarkup(row_width=2)
    for button in menuCategories:
        menuButtons.insert(button)

    menuButtons.row()
    menuButtons.insert(types.InlineKeyboardButton("Ничего", callback_data="discard"))
    logger.debug(f"{create_categories_buttons.__name__} finished")

    return menuButtons