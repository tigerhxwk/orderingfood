#!/bin/python3

from bs4 import BeautifulSoup
import requests, json

def GetPage(URL):
	try:
		page = requests.get(URL, timeout=30)
	except page.exceptions.Timeout:
		print("Connection is timed out")
		return -1

	return page.content

def ParsePage(PAGE):

	index = 0

	soup = BeautifulSoup(PAGE, 'html.parser')

	ItemsData = dict()
	result = dict()

	table = soup.select('.corp-table > .corp-category')

	for items in table:

		for item in items.select('.corp-item-wrap >.corp-item'):

			ItemData = { 'name': [], 'price': [], 'info': [] }

			for name in item.select('.item-name > b'):
				ItemData['name'].append(name.string)

			for price in item.select('.full-portion > .item-price > span'):
				ItemData['price'].append(price.string)

			for description in item.select('.item-info'):
				ItemData['info'].append(description.string)

			ItemsData.update({index: ItemData})
			index = index + 1

		result.update({items.select_one('.corp-category > h2').string: ItemsData.copy()})
		ItemsData.clear()

	return result

def main():
	
	jsonString = json.dumps(ParsePage(GetPage('https://corp.olivkafood.ru/')), indent=4, ensure_ascii=False)

	jsonFile = open("data.json", "w")
	jsonFile.seek(0)
	jsonFile.truncate()
	jsonFile.write(jsonString)
	jsonFile.close()

	return 0

if __name__ == "__main__":
	main()
