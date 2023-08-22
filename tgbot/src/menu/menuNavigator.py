
# Usage:
#       on Menu button handler call newChat to drop all values to default
#       on category selection call setCategory
#       after printing all items for page call setPageItemCount
#       after calling setPageItemCount it's necessary to call setPageCounter with actual amount of pages
#       amount of pages depends on what user selects from navigation buttons below item's list

class menuNav:
    __BreadCrumbs = dict ()
    __logger = None
    def __init__(self, logger = None):
        if logger != None:
            self.__logger = logger
        return

    def newChat (self, chatId):
        if chatId not in self.__BreadCrumbs.keys():
            self.__BreadCrumbs[chatId] = dict ()

        self.__BreadCrumbs[chatId]['category'] = ''
        self.__BreadCrumbs[chatId]['currPrintCount'] = 0
        self.__BreadCrumbs[chatId]['pageCounter'] = 0
        # pages dict contains amount of items per each page
        self.__BreadCrumbs[chatId]['pages'] = dict ()

        return


    def setCategory (self, chatId, value = ''):
        if chatId in self.__BreadCrumbs.keys():
            self.__BreadCrumbs[chatId]['category'] = value
            self.__BreadCrumbs[chatId]['pages'].clear()
            self.__BreadCrumbs[chatId]['currPrintCount'] = 0
            self.__BreadCrumbs[chatId]['pageCounter'] = 0

    def getCategory (self, chatId):
        if chatId in self.__BreadCrumbs.keys():
            return self.__BreadCrumbs[chatId]['category']


    def __addToCurrPrintCount (self, chatId, value = 10):
        if chatId in self.__BreadCrumbs.keys():
            self.__innerDebug(f"adding sent {value} to printcount {self.__BreadCrumbs[chatId]['currPrintCount']}")
            self.__BreadCrumbs[chatId]['currPrintCount'] += value

    def __rmFromCurrPrintCount (self, chatId, value):
        if chatId in self.__BreadCrumbs.keys():
            self.__innerDebug(f"removing deleted {value} from printcount "
                              f"{self.__BreadCrumbs[chatId]['currPrintCount']}")
            self.__BreadCrumbs[chatId]['currPrintCount'] -= value


    def setPageItemCount (self, chatId, page, itemcount):
        if chatId in self.__BreadCrumbs.keys():
            self.__BreadCrumbs[chatId]['pages'][page] = itemcount
            self.__innerDebug(f'set count {itemcount} for page {page}')


    def getPageItemCount (self, chatId, page)-> int:
        if chatId in self.__BreadCrumbs.keys():
            if page in self.__BreadCrumbs[chatId]['pages'].keys ():
                return self.__BreadCrumbs[chatId]['pages'][page]


    def setPageCounter (self, chatId, value):
        self.__innerDebug(f'value {value} is passed to setPageCounter')
        if chatId in self.__BreadCrumbs.keys():
            if value < self.__BreadCrumbs[chatId]['pageCounter']:
                if value in self.__BreadCrumbs[chatId]['pages'].keys():
                    self.__innerDebug(f'value {value} is found in keys')
                    self.__rmFromCurrPrintCount(chatId, self.__BreadCrumbs[chatId]['pages'][value])
                    if value + 1 in self.__BreadCrumbs[chatId]['pages'].keys():
                        self.__rmFromCurrPrintCount(chatId, self.__BreadCrumbs[chatId]['pages'][value + 1])

                else:
                    self.__innerDebug(f'value {value} is not found in keys')
                    if value == 0:
                        # this will reset all data for current category for chat
                        self.setCategory(chatId)
                        return
                    else:
                        # there's an error
                        self.__innerDebug(f'total bullshit happened')

            self.__BreadCrumbs[chatId]['pageCounter'] = value
            self.__innerDebug(f"set pagecounter {value}, pages breadcrumbs {self.__BreadCrumbs[chatId]['pages']}")
            self.__addToCurrPrintCount(chatId, self.__BreadCrumbs[chatId]['pages'][value])


    def getPageCounter (self, chatId):
        if chatId in self.__BreadCrumbs.keys():
            return self.__BreadCrumbs[chatId]['pageCounter']

    def getCurrPrintCount (self, chatId)->int:
        if chatId in self.__BreadCrumbs.keys():
            return self.__BreadCrumbs[chatId]['currPrintCount']

    def __innerDebug (self, message=''):
        if self.__logger != None:
            self.__logger.debug (f'menu_nav:{message}')
