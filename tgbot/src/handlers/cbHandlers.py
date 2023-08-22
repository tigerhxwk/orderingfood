from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from init_bot import foodBot, foodBotDispatcher, logger
from handlers.msghandlers import starter as starter
from menu import buttons_builder
from cart import cartApi
from menu.menuNavigator import menuNav

globalCart = cartApi.Cart()
PRINT_LIMITER = 10
categoryButtons = None
parsedMenu = None
naviStorage = menuNav (logger)

def argument_overloader (input):
    if isinstance(input, types.CallbackQuery):
        selector = input.message.chat
        message_id = input.message.message_id
    else:
        selector = input.chat
        message_id = input.message_id

    return selector.username, selector.first_name, selector.last_name, selector.id, message_id

async def category_callback (callback :types.CallbackQuery):
    global parsedMenu, naviStorage

    data = callback.data
    logger.debug (f"{category_callback.__name__} received {data}")
#     this callback handles callback data that begins with category_<category>

    await foodBot.sendMessage(callback, "Выбирай:", clear=True)

    naviStorage.setCategory(callback.message.chat.id, data[9:])

    pageCounter = naviStorage.getPageCounter(callback.message.chat.id)
    pageCounter += 1
    await send_category_contents (callback, parsedMenu[naviStorage.getCategory(callback.message.chat.id)],
                                  naviStorage.getCurrPrintCount(callback.message.chat.id), pageCounter)


async def menu_printer(callback : types.CallbackQuery):
    global naviStorage
    # Kinda function overload, callback_query_handler gives here CallbackQuery,
    # but message_handler gives here message, that is nested field of CallbackQuery
    username, first_name, last_name, chat_id, message_id = argument_overloader (callback)
    logger.debug(f"user {username} {first_name} {last_name} selected menu")
    naviStorage.newChat(chat_id)
    await foodBot.sendMessage(callback, "Выбирай категорию:", markup=categoryButtons, clear=True)

async def discard (callback : types.CallbackQuery):
    global globalCart, naviStorage
    #need to make cart and 'end' features
    username, first_name, last_name, chat_id, message_id = argument_overloader(callback)
    logger.debug(f"user {username} {first_name} {last_name} changed his mind")
    naviStorage.setCategory(chat_id)
    globalCart.clearCart(chat_id)
    await foodBot.sendMessage(callback, "Будем ждать снова!", clear=True)


async def show_cart (callback : types.CallbackQuery):
    username, first_name, last_name, chat_id, message_id = argument_overloader(callback)
    global globalCart, parsedMenu

    logger.debug(f"user {username} {first_name} {last_name} requested cart")

    cartLen = globalCart.getLen (chat_id)

    if cartLen == 0:
        await foodBot.sendMessage(callback, "В корзине ничего нет...", clear=True)
    else:
        await foodBot.sendMessage(callback, "Твой заказ:", clear=True)
        for itemId in range(cartLen):
            item = globalCart.getItem(chat_id, itemId)
            for category in parsedMenu:
                logger.debug (f"checking category {category} for matching {item}")
                menuItem = parsedMenu[category].keys()
                if str(item) in menuItem:
                    logger.debug (f"found match for {item} in {category}")
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    markup.insert(types.InlineKeyboardButton("Удалить", callback_data=f"rm_{item}"))
                    position = parsedMenu[category][str(item)]
                    names = position['name']
                    prices = position['price']
                    info = position['info']
                    for name in names:
                        stringToSend = f"*{name}:*\n"
                    for instance in info:
                        stringToSend += f"{instance}\n"
                    stringToSend += "Цена: "
                    for price in prices:
                        stringToSend += f"{price}"
                    logger.debug(f"msg to send is {stringToSend}")

                    await foodBot.sendMessage(callback, stringToSend, markup=markup)
                    break


    if isinstance(callback, types.CallbackQuery):
        await starter(callback.message)
    else:
        await starter(callback)

async def nothing_handler (callback : types.CallbackQuery):
    _, first_name, _, chat_id, message_id = argument_overloader(callback)
    global globalCart

    logger.debug(f"{first_name} selected nothing")
    globalCart.clearCart(chat_id)
    await menu_printer(callback)

# start argument is used to skip already printed positions
async def send_category_contents (callback : types.CallbackQuery, Menu : dict (), start, pageCounter):
    global naviStorage
    counter = 0
    logger.debug(f"starter position {start} pagecounter {pageCounter}")
    await foodBot.sendMessage(callback, f"Страница:{pageCounter}", silent=True, clear=True)
    for key in Menu.keys():
        if counter < start:
            counter += 1
            continue
        if counter >= start + PRINT_LIMITER or key == list(Menu)[-1]:
            markup = types.InlineKeyboardMarkup ()
            if key == list(Menu)[-1]:
                markup.insert(types.InlineKeyboardButton("Меню", callback_data=f"return_from_contents_{counter}"))
            else:
                markup.insert(types.InlineKeyboardButton("Далее", callback_data="next"))
            if start == 0:
                markup.insert(types.InlineKeyboardButton("Меню", callback_data=f"return_from_contents_{counter}"))
            else:
                markup.insert(types.InlineKeyboardButton("Назад", callback_data="previous"))
            await foodBot.sendMessage(callback, "Или:", markup=markup)
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

        await foodBot.sendMessage(callback, stringToSend, markup = markup)
        counter += 1

    naviStorage.setPageItemCount(callback.message.chat.id, pageCounter, counter - start)
    naviStorage.setPageCounter(callback.message.chat.id, pageCounter)
    logger.debug(f'set pageitemcount {counter - start}, pagecounter {pageCounter}'
                 f' currprint {naviStorage.getCurrPrintCount(callback.message.chat.id)} ')


async def return_from_contents (callback : types.CallbackQuery):
    printedCounter = int(callback.data[21:])
    logger.debug (f"received return with {printedCounter} printed positions")

    await menu_printer(callback)

async def next_content (callback : types.CallbackQuery):
    global parsedMenu, naviStorage
    logger.debug(f"user {callback.message.chat.username} {callback.message.chat.first_name}"
                 f" {callback.message.chat.last_name} requested next contents")

    await send_category_contents (callback, parsedMenu[naviStorage.getCategory(callback.message.chat.id)],
                                  naviStorage.getCurrPrintCount(callback.message.chat.id),
                                  naviStorage.getPageCounter(callback.message.chat.id) + 1)

async def previous_content (callback : types.CallbackQuery):
    global parsedMenu, naviStorage
    logger.debug (f"handling previous contents for current print count {naviStorage.getCurrPrintCount(callback.message.chat.id)}")
    # gotta make per-page counters
    #  curr print count - prev-page actual print count
    # pagecounter --
    chatId = callback.message.chat.id
    currPrintCount = (naviStorage.getCurrPrintCount (chatId) -
                      naviStorage.getPageItemCount(chatId, naviStorage.getPageCounter(chatId)) -
                      naviStorage.getPageItemCount(chatId, naviStorage.getPageCounter(chatId) - 1))

    logger.debug (f'oldprintCount {naviStorage.getCurrPrintCount (chatId)}, new {currPrintCount}')
    pageCounter = naviStorage.getPageCounter(chatId) - 1

    await send_category_contents (callback, parsedMenu[naviStorage.getCategory(chatId)],
                                  currPrintCount, pageCounter)


async def add_to_cart (callback : types.CallbackQuery):
    global globalCart
    logger.debug (f"{add_to_cart.__name__} received cbdata {callback.data} from chat {callback.message.chat.id}")
    item = callback.data[4:]
    globalCart.addToCart(callback.message.chat.id, item)

async def remove_from_cart (callback : types.CallbackQuery):
    global globalCart
    logger.debug (f"{remove_from_cart.__name__} received cbdata {callback.data}")
    item = callback.data[4:]
    globalCart.rmItemFromCart (callback.message.chat.id, item)

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
    foodDispatcher.register_callback_query_handler(add_to_cart, Text(startswith="add_"))
    foodDispatcher.register_callback_query_handler(remove_from_cart, Text(startswith="rm_"))
    logger.debug ("registered callbacks and created buttons")
