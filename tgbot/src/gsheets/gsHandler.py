import string

import gspread
from gspread_formatting import *
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials
from string import ascii_uppercase
import os

colNames = ["Имя", "Название", "Стоимость",
            "Стоимость всего", "Итого", "По чеку",
            "Итого факт", "Всего факт", "Доставка"]
class gHandler:
    __sheet = None
    __ws_list = dict ()
    __logger = None
    def __init__(self, logger = None):
        if logger != None:
            self.__logger = logger
        scopes = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive.file',
                    'https://www.googleapis.com/auth/drive']

        cred_file = os.getcwd() + "/tgbot/src/gsheets/cred.json"
        # credentials = ServiceAccountCredentials.from_json_keyfile_name('gsheets/olivkafoodv2-1cd18a3a7cde.json',
        #                                                                scopes)

        credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file,
                                                                        scopes)
        gc = gspread.authorize(credentials)

        sheetId = "1ml9ZUkn-Wt_DTZhQDYUUaBgrqTiXApkt2D0i6tA-qZU"
        self.__sheet = gc.open_by_key(sheetId)
        try:
            ws_list = self.__sheet.worksheets()
        except:
            self.__innerDebug ("no access to spreadsheet")

        for ws in ws_list:
            self.__ws_list[str(ws).split()[1].replace("'",'')] = ws
        self.__innerDebug(self.__ws_list)
    __updates_list = dict ()


    def addWorkSheet (self, name, rows = 100, cols = 11):
        self.__innerDebug(f"checking if {name} is in {self.__ws_list}")
        if name not in self.__ws_list.keys():
            self.__innerDebug("it's not")
            ws = self.__sheet.add_worksheet(title=name, rows=rows, cols=cols)
            self.__ws_list[name] = ws
            self.__innerDebug (self.__ws_list)
            columns = list ()
            for column in string.ascii_uppercase:
                if column == 'J':
                    break
                columns.append(column)

            self.__innerDebug(columns)
            for index in range(1, len(columns) + 1):
                self.__ws_list[name].update(f"{columns[index - 1]}{1}", colNames[index - 1])

            set_column_width(self.__ws_list[name], 'A', 200)
            set_column_width(self.__ws_list[name], 'B', 350)

    def next_available_row(self, name, cols_to_sample=2):
        # looks for empty row based on values appearing in 1st N columns
        cols = self.__ws_list[name].range(1, 1, self.__ws_list[name].row_count, cols_to_sample)
        return max([cell.row for cell in cols if cell.value]) + 1


    def updateSingleCell (self, sheetId, cell, value):
        if sheetId in self.__ws_list.keys():
            self.__ws_list[sheetId].update(cell, value)


    def updateListOfCells (self, sheetId, cellsAndValues = dict ()):
        if sheetId in self.__ws_list.keys():
            for cell in cellsAndValues.keys():
                self.__ws_list[sheetId].update(cell, cellsAndValues[cell])


    def prepareForUpdate (self, sheetId, cell, value):
        if sheetId in self.__ws_list.keys():
            if sheetId not in self.__updates_list.keys():
                self.__updates_list[sheetId] = []

            self.__innerDebug(cell)
            cellRow = int(cell[1:])
            self.__updates_list[sheetId].append (Cell ((cellRow),
                                                        self.__convertA1ToNum(cell), value))


    def mergeNameColumn (self, sheetId, startRow, endRow):
        if sheetId in self.__ws_list.keys():
            self.__ws_list[sheetId].merge_cells(f"A{startRow}:A{endRow}")
            fmt = cellFormat(horizontalAlignment='CENTER', verticalAlignment='MIDDLE')
            format_cell_range(self.__ws_list[sheetId], f"A{startRow}:A{endRow}", fmt)

    def __convertA1ToNum (self, cell):
    #      cell comes here as "A1", so we gotta convert 'A' to 1, 'B' to 2 etc
    #  going C-style, for sure
        index = 1
        for column in string.ascii_uppercase:
            if column == cell[:1]:
                return int(index)
            index += 1


    def runUpdate (self, sheetId):
        if sheetId in self.__ws_list.keys() and sheetId in self.__updates_list.keys():
            self.__innerDebug(f"run update {self.__updates_list[sheetId]}")
            self.__ws_list[sheetId].update_cells(self.__updates_list[sheetId])
            self.__updates_list[sheetId].clear()


    def getCellValue(self, sheetId, cell):
        if sheetId in self.__ws_list.keys():
            value = self.__ws_list[sheetId].acell(cell).value
            if value != None:
                return value

        return 0


    def __innerDebug (self, message=''):
        if self.__logger != None:
            self.__logger.debug (f'gsHandler:{message}')
