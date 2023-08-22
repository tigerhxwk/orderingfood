from init_bot import logger

class Cart:
    # cart represents dict of arrays where key is chat id and values are items from menu
    __cart = dict ()
    def __init__(self):
        logger.debug ("cart is initialized")


    def addToCart (self, userId, item):
        intItem = int (item)
        if userId in self.__cart:
            self.__cart[userId].append (intItem)
            logger.debug (f"added {intItem} for user {userId} to cart")
        else:
            logger.debug (f"created cart and added {intItem} for user {userId} to cart")
            self.__cart[userId] = list ()
            self.__cart[userId].append (intItem)


    def rmItemFromCart (self, userId, item):
        if userId in self.__cart:
            self.__cart[userId].remove(item)
            logger.debug (f"removed {item} from user {userId} cart")
        else:
            logger.debug ("attempted to delete something that is missing in cart")

    def clearCart (self, userId):
        if userId in self.__cart:
            del self.__cart[userId]
            logger.debug (f"cleared cart for user {userId}")
        else:
            logger.debug ("attempted to clear non-present cart")


    def getLen (self, userId)-> int:
        if userId in self.__cart:
            logger.debug (f"len of cart for chat {userId} is {len (self.__cart[userId])}")
            return len (self.__cart[userId])

        logger.debug (f"len of cart for chat {userId} is 0")
        return 0


    def getItem (self, userId, itemdId):
        if userId in self.__cart:
            if itemdId >= 0 and itemdId < len(self.__cart[userId]):
                logger.debug (f"returning cart item {self.__cart[userId][itemdId]} for chat {userId}, itemid {itemdId}")
                return self.__cart[userId][itemdId]

        logger.debug (f"Invalid data: {userId} or {itemdId}")
        return -1
