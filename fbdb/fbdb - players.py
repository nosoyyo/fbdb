#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 再抓人

__author__ = 'nosoyyo'

import os
import csv
import time
import random
import requests
from bs4 import BeautifulSoup

# constants
k = 0
img_count = 0
root_dir = os.getcwd()
print('started at ' + str(time.time()))
brand_list = {'Adi': 'Adidas', 'Conco' : 'Concord', 'Conca' : 'Concave', 'Nik': 'Nike', 'Asi': 'Asics', 'Dia': 'Diadora', 'Ree': 'Reebok', 'Miz': 'Mizuno', 'New': 'New Balance', 'Pum': 'Puma', 'Umb': 'Umbro', 'Und': 'Under Armour', 'Jom': 'Joma', 'Lot': 'Lotto'}

# 循环
i = 2324
for i in range(2325, 9999):
    print('now...', end="")
    #拼接 url, rnd_referer
    url = 'http://www.footballbootsdb.com/player/*/' + str(i)
    rnd_referer = 'http://www.footballbootsdb.com/boot/*/' + str(int(random.uniform(1, 18000)))

    #headers
    headers = {'Host' : 'www.footballbootsdb.com', 'Connection' : 'keep-alive', 'Cache-Control' : 'max-age=0', 'Upgrade-Insecure-Requests' : '1', 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Referer' : rnd_referer, 'Accept-Encoding' : 'gzip, deflate, sdch', 'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,es;q=0.2,it;q=0.2', 'Cookie' : '_ga=GA1.2.1545417116.1490602283'}
    
    #抓取 HTML
    response = requests.get(url, headers = headers, )
    if response.status_code == 200:
        print('we\'re...', end="")
        soup = BeautifulSoup(response.text, "html.parser")
        current_url = soup.head.link['href']

        player = soup.h1.string
        boots_1617 = str(soup.h2).split(":")[-1].replace("\t</h2","").strip()
        if boots_1617.split(" ")[0][:3] == 'New':
                brand = brand_list['New']
        elif boots_1617.split(" ")[0][:5] == 'Conca':
            brand = brand_list['Conca']
        elif boots_1617.split(" ")[0][:5] == 'Conco':
            brand = brand_list['Conco']
        elif boots_1617.split(" ")[0][:5] == 'Under':
            brand = brand_list['Und']
        else:
            brand = boots_1617.split(" ")[0]
        print(brand + '...', end="")
        model = boots_1617.replace(brand + " ", "")
        model = model.replace('/', ' SLASH ')
        print(model +'. \n')

        # 写 csv
        print('done. \n')
        os.chdir(root_dir)
        f = open('fbdb_player.csv', 'a')
        headers = ['Player', 'Brand', 'Model', 'Price', 'Players']
        #f_csv = csv.DictWriter(f, headers)
        #f_csv.writeheader()

        rows_dict = [{'Player' : player, 'Brand' : brand, 'Model' : model, 'Price' : 0,}]
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerows(rows_dict)
        f.close()
        print('csv wrote. \n')

        # 打印
        print("So we now have #" + str(i) + " " + brand + " " + model + " all done." + '\n' + current_url + "\n" + "referer:" + rnd_referer + '\n')

        # 延时
        #rnd_time_interval = random.uniform(0.1, 1)
        #time.sleep(rnd_time_interval)
    
    else:
        print('blocked by boot #' + str(i) + " . So we happily go for the next." + '\n')
        #it seems not necessary to sleep for now for here.
        #time.sleep(0.5)