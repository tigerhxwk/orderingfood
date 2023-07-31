#!/bin/python3

from bs4 import BeautifulSoup
import requests, json

def GetPage(URL):
	try:
		page = requests.get(URL, timeout=10)
	except page.exceptions.Timeout:
		print("Connection is timed out")
		return -1

	return page.content

def ParsePage(PAGE):
	result = {'category' : [], 'items' : []}

	soup = BeautifulSoup(PAGE, 'html.parser')

	table = soup.select('.corp-table > .corp-category')

	for items in table:
		categoryData = {'names' : [], 'prices': [], 'info' : []}

		for name in items.select('.item-name > b'):
			categoryData['names'].append(name.string)

		for price in items.select('.full-portion > .item-price > span'):
			categoryData['prices'].append(price.string)

		for description in items.select('.item-info'):
			categoryData['info'].append(description.string)

		result['category'].append(items.select_one('.corp-category > h2').string)
		result['items'].append(categoryData)

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
