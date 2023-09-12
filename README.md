# orderingfood
Telegram-bot that is used as user-friendly API between users and non-user-friendly web-site

## Functionality
![Web-site screencshot](https://github.com/tigerhxwk/orderingfood/blob/master/site.png)

It's really uncomfortable to order food like this, not to mention mobile (unoptimized) version of this web-site, so bot uses parsed web-site as json-file made of parsed tags.
Parsed tags consist of category used to represent menu at first as categories, positions of it's category and positions' descriptions and prices.
Each parsed position is consecutive numbered because every "Add" button has it's own callback data, so using indexes make it easy to parse callback data from user and also helps to parse json quickly.
Docker container uses cron to call parser script each day at specific time and restart bot.
After being started bot creates menu out of json-file which is a dictionary of dictionaries of dictionaries. When user selects menu, bot sends categories,
then sends positions of selected category with "Add" button that allows to add position to cart.
Each user has his own cart depending on chat-Id.
When user is good to go, "Order" button sends selected positions to Google Sheets.

## Demo
![Demo](https://github.com/tigerhxwk/orderingfood/blob/master/demo.gif)

## Usage:
* `make`:  build docker image
* `make up`:    build docker image and run bot
* `make clean`: remove all build images
* `make shell`: build and spawn shell in container

