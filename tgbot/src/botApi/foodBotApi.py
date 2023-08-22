from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

class FoodBot:
    __botIsUpAndRunning = False
    __foodBot = 0
    __footBotDispatcher = 0
    __sent_msg_counter = dict ()
    __logger = None
    def __init__(self, key, logger = None):
        if logger != None:
            self.__logger = logger

        try:
            self.__foodBot = Bot(key)
        except:
            self.__innerDebug (f"unable to start bot")
            return

        self.__foodBotDispatcher = Dispatcher(self.__foodBot)
        self.__botIsUpAndRunning = True
        self.__innerDebug (f"bot is up and running")


    def GimmeTheBot (self):
        if self.__botIsUpAndRunning == True:
            return (self.__foodBot, self.__foodBotDispatcher)
        else:
            self.__innerDebug (f'bot is not running')
            return 0,0


    def __argumentOverloader(self, input):
        if isinstance(input, types.CallbackQuery):
            selector = input.message.chat
            message_id = input.message.message_id
        else:
            selector = input.chat
            message_id = input.message_id

        return selector.id, message_id

    async def __clearCb (self, callback : types.CallbackQuery):
        try:
            await callback.message.delete()
        except:
            self.__innerDebug (f"Unable to delete message {callback.message.message_id}"
                               f" from chat {callback.message.chat.id}")
    async def sendMessage(self, meta_data, message="Sample text", clear = False,
                    markup = None, silent = True, parsemode = "Markdown"):
        chat_id, curr_msg_id = self.__argumentOverloader(meta_data)
        if clear == True:
            self.__innerDebug (f"current sent msgs amount is {self.__sent_msg_counter[chat_id]}")
            if chat_id in self.__sent_msg_counter:
                for msg_counter in range (self.__sent_msg_counter[chat_id]):
                    try:
                        await self.__foodBot.delete_message(chat_id, curr_msg_id - msg_counter)
                    except:
                        self.__innerDebug (f"Unable to delete message {curr_msg_id - msg_counter} from chat {chat_id}")
                        if isinstance(meta_data, types.CallbackQuery):
                            await self.__clearCb(meta_data)

                self.__sent_msg_counter[chat_id] = 0

        if markup == None:
            await self.__foodBot.send_message(chat_id, message, parse_mode=parsemode,
                                              disable_notification=silent)
        else:
            await self.__foodBot.send_message(chat_id, message, parse_mode=parsemode,
                                              reply_markup=markup, disable_notification=silent)

        if chat_id in self.__sent_msg_counter:
            self.__sent_msg_counter[chat_id] = self.__sent_msg_counter[chat_id] + 1
        else:
            self.__sent_msg_counter[chat_id] = 1

    def __innerDebug (self, message=''):
        if self.__logger != None:
            self.__logger.debug (f'foodbot:{message}')