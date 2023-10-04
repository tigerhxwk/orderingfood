#!/bin/bash

killall -s 2 python
rm -f data.json
python /parser/parser.py
python /tgbot/src/aiobot.py $TKEY
