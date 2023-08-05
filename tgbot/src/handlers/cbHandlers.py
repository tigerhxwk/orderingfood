from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from init_bot import foodBot, foodBotDispatcher, logger
from handlers.msghandlers import starter as starter
from menu import buttons_builder

PRINT_LIMITER = 10
categoryButtons = None
parsedMenu = None
currentCategory = None
currentPrintCount = None
lastPrintCount = None

def argument_overloader (input):
    if isinstance(input, types.CallbackQuery):
        selector = input.message.chat
        message_id = input.message.message_id
    else:
        selector = input.chat
        message_id = input.message_id

    return selector.username, selector.first_name, selector.last_name, selector.id, message_id

async def category_callback (callback :types.CallbackQuery):
    global parsedMenu, currentCategory, currentPrintCount

    data = callback.data
    logger.debug (f"{category_callback.__name__} received {data}")
#     this callback handles callback data that begins with category_<category>
    try:
        await callback.message.delete()
    except:
        logger.debug(f"Unable to delete message {callback.message.message_id} from chat {callback.message.chat.id}")

    await foodBot.send_message(callback.message.chat.id, "Выбирай:")
    currentCategory = data[9:]
    currentPrintCount = 0
    await send_category_contents (callback, parsedMenu[currentCategory], currentPrintCount)


async def menu_printer(callback : types.CallbackQuery):
    global categoryButtons, currentPrintCount, lastPrintCount, currentCategory
    # Kinda function overload, callback_query_handler gives here CallbackQuery,
    # but message_handler gives here message, that is nested field of CallbackQuery
    username, first_name, last_name, chat_id, message_id = argument_overloader (callback)
    logger.debug(f"user {username} {first_name} {last_name} selected menu")

    try:
        await foodBot.delete_message(chat_id, message_id)
    except:
        logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")
    logger.debug(f'current message id is {message_id}')

    currentPrintCount = 0
    currentCategory = ''
    lastPrintCount = 0
    await foodBot.send_message(chat_id, "Выбирай категорию:", reply_markup=categoryButtons)

async def discard (callback : types.CallbackQuery):
    #need to make cart and 'end' features
    global  currentPrintCount, lastPrintCount
    username, first_name, last_name, chat_id, message_id = argument_overloader(callback)
    logger.debug(f"user {username} {first_name} {last_name} changed his mind")
    if lastPrintCount != 0:
        for _ in range (0, lastPrintCount + 3):
            try:
                await foodBot.delete_message(chat_id, message_id - _)
            except:
                logger.debug(
                    f"Unable to delete message {message_id - _} from chat {chat_id}")
    else:
        try:
            await foodBot.delete_message(chat_id, message_id)
        except:
            logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")
        try:
            await foodBot.delete_message(chat_id, message_id - 1)
        except:
            logger.debug(f"Unable to delete message {message_id - 1} from chat {chat_id}")

    await foodBot.send_message(chat_id, "Будем ждать снова!")


async def show_cart (callback : types.CallbackQuery):
    username, first_name, last_name, chat_id, message_id = argument_overloader(callback)
    logger.debug(f"user {username} {first_name} {last_name} requested cart")
    try:
        await foodBot.delete_message(chat_id, message_id)
    except:
        logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")
    await foodBot.send_message(chat_id, "Корзина по техническим причинам недоступна")

    if isinstance(callback, types.CallbackQuery):
        await starter(callback.message)
    else:
        await starter(callback)

async def nothing_handler (callback : types.CallbackQuery):
    _, first_name, _, chat_id, message_id = argument_overloader(callback)
    try:
        await foodBot.delete_message(chat_id, message_id)
    except:
        logger.debug(f"Unable to delete message {message_id} from chat {chat_id}")
    try:
        await foodBot.delete_message(chat_id, message_id - 1)
    except:
        logger.debug(f"Unable to delete message {message_id - 1} from chat {chat_id}")

    logger.debug(f"{first_name} selected nothing")

    await menu_printer(callback)

# start argument is used to skip already printed positions, 11 is counted by start + <how_many_to_print> + 1
# <how_many_to_print> is PRINT_LIMITER for now
async def send_category_contents (callback : types.CallbackQuery, Menu : dict (), start):
    # delete previously sent messages
    global currentPrintCount, lastPrintCount
    if start < 0:
        logger.debug (f"whoopsie, incorrect print value {start}")
        return
    if lastPrintCount != 0 and lastPrintCount != None:
        for _ in range (0, lastPrintCount + 1):
            try:
                await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - _)
            except:
                logger.debug(
                    f"Unable to delete message {callback.message.message_id - _} from chat {callback.message.chat.id}")
        currentPrintCount -= lastPrintCount

    counter = 0
    for key in Menu.keys():
        if counter < start:
            counter += 1
            continue
        elif counter >= start + PRINT_LIMITER or key == list(Menu)[-1]:
            markup = types.InlineKeyboardMarkup ()
            if key == list(Menu)[-1]:
                markup.insert(types.InlineKeyboardButton("Меню", callback_data=f"return_from_contents_{counter}"))
            else:
                markup.insert(types.InlineKeyboardButton("Далее", callback_data="next"))
            if start == 0:
                markup.insert(types.InlineKeyboardButton("Меню", callback_data=f"return_from_contents_{counter}"))
            else:
                markup.insert(types.InlineKeyboardButton("Назад", callback_data="previous"))
            await foodBot.send_message(callback.message.chat.id, "Или:", reply_markup=markup, disable_notification=True)
            break

        names = Menu[key]['name']
        prices = Menu[key]['price']
        info = Menu[key]['info']

        for name in names:
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.insert(types.InlineKeyboardButton("+", callback_data=f"add_{key}"))
            markup.insert(types.InlineKeyboardButton("-", callback_data=f"rm_{key}"))
            logger.debug (f"created cart-control buttons for key {key}")
            stringToSend = f"*{name}:*\n"
            for instance in info:
                stringToSend += f"{instance}\n"
            stringToSend += "Цена: "
            for price in prices:
                stringToSend += f"{price}"

        await foodBot.send_message(callback.message.chat.id, stringToSend, parse_mode = "Markdown",
                                   reply_markup = markup, disable_notification=True)
        counter += 1
    lastPrintCount = counter - start
    currentPrintCount += lastPrintCount


async def return_from_contents (callback : types.CallbackQuery):
    global currentPrintCount, lastPrintCount
    printedCounter = int(callback.data[21:])
    logger.debug (f"received return with {printedCounter} printed positions")
    if lastPrintCount is None:
        rangeLimiter = PRINT_LIMITER
    else:
        rangeLimiter = lastPrintCount
    for _ in range(0, rangeLimiter + 2):
        try:
            await foodBot.delete_message(callback.message.chat.id, callback.message.message_id - _)
        except:
            logger.debug(
                f"Unable to delete message {callback.message.message_id - _} from chat {callback.message.chat.id}")
    currentPrintCount = 0
    lastPrintCount = 0
    await menu_printer(callback)

async def next_content (callback : types.CallbackQuery):
    global parsedMenu, currentCategory, currentPrintCount
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}"
                 f" {callback.message.chat.last_name} requested next contents")
    await send_category_contents (callback, parsedMenu[currentCategory], currentPrintCount)

async def previous_content (callback : types.CallbackQuery):
    global parsedMenu, currentCategory, currentPrintCount
    logger.debug (f"handling previous contents for current print count {currentPrintCount}")
    currentPrintCount -= lastPrintCount
    await send_category_contents (callback, parsedMenu[currentCategory], currentPrintCount)


def register_callbacks_handler (foodDispatcher : Dispatcher, Menu : dict ()):
    global categoryButtons, parsedMenu
    parsedMenu = Menu
    foodDispatcher.register_callback_query_handler(menu_printer, Text(equals="menu"))
    foodDispatcher.register_callback_query_handler(nothing_handler, Text(equals="discard"))
    foodDispatcher.register_callback_query_handler(show_cart, Text(equals="show_cart"))
    foodDispatcher.register_callback_query_handler(category_callback, Text(startswith="category_"))
    foodDispatcher.register_callback_query_handler(return_from_contents,
                                   Text(startswith="return_from_contents_"))
    foodDispatcher.register_callback_query_handler(next_content, Text(equals="next"))
    foodDispatcher.register_callback_query_handler(previous_content, Text(equals="previous"))
    categoryButtons = buttons_builder.create_categories_buttons(parsedMenu)
    foodDispatcher.register_message_handler(menu_printer, commands='show_menu')
    foodDispatcher.register_message_handler(discard, commands='discard')
    foodDispatcher.register_message_handler(show_cart, commands='show_cart')
    logger.debug ("registered callbacks and created buttons")
