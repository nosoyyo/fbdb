#!/usr/bin/env python
# -*- coding: utf-8 -*-


# get mongodb keys as keys
# get prices everyday
# try exceptions

__author__ = 'nosoyyo'
import requests
from bs4 import BeautifulSoup
import gc
import csv
import json
import time
import random
import pymongo

for i in range()

    #get player_resource_id for XHR 
    prid = soup.select('div#page-info')[0].attrs['data-player-resource']

    # price module
    xhr = 'https://www.futbin.com/18/playerPrices?player=' + prid
    xhr_headers = {'accept' : 'application/json, text/javascript, */*; q=0.01', 'accept-encoding' : 'gzip', 'accept-language' : 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6,it;q=0.5', 'cookie' : '__cfduid=d7b229e8a67f2f970f39f93f8fd5f32201515132865; PHPSESSID=8352d14773681915ba9f9fca29404062; _ga=GA1.2.1931620846.1515132876; xbox=true; ps=true; pc=true; OX_plg=pm; __gads=ID=17b3c1a533b9ce27:T=1515132916:S=ALNI_MbkNMV175g7e6ObdaLnT6HhZFUZDw; cookieconsent_dismissed=yes; platform=xone; platform_type=console; _gid=GA1.2.1661263958.1515391404; _dm_sync=true; OX_sd=7; sc_is_visitor_unique=rx9767571.1515397301.7158A1C2145D4F80CD39A3074984500A.6.4.2.2.2.2.2.2.1', 'referer' : url, 'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'x-newrelic-id' : 'VQEEU1NaDBADVlhUAQAHXg==', 'x-requested-with' : 'XMLHttpRequest'}
    xhr_response = requests.get(xhr, headers = xhr_headers)
    price_dict = json.loads(xhr_response.text)

    # deal with prices, get an anyway price for the moment
    price_xbox = price_dict[prid]['prices']['xbox']['LCPrice']
    price_ps = price_dict[prid]['prices']['ps']['LCPrice']
    price_pc = price_dict[prid]['prices']['pc']['LCPrice']

    # update'em in MongoDB
    client = pymongo.MongoClient("localhost", 27017)
    db = client.fut18
    players = db["players"]