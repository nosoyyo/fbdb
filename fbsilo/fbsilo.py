#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 

__author__ = 'nosoyyo'

import os
import csv
import time
import random
import requests
from bs4 import BeautifulSoup

img_count = 0
root_dir = os.getcwd()
print('started at ' + str(time.time()))
brand_list = {'Adi': 'Adidas', 'Conco' : 'Concord', 'Conca' : 'Concave', 'Nik': 'Nike', 'Asi': 'Asics', 'Dia': 'Diadora', 'Ree': 'Reebok', 'Miz': 'Mizuno', 'New': 'New Balance', 'Pum': 'Puma', 'Umb': 'Umbro', 'Und': 'Under Armour', 'Jom': 'Joma', 'Lot': 'Lotto'}

brand = ""
model = ""
model = model.replace('/', ' SLASH ') #just in case
launch_date = ""
price = ""
ground_type = []
material = ""
weight = ""
players = []

class Info:
    def __init__(self, brand, model, launch_date, price, ground_type, material, weight, players):
        self.brand = brand
        self.model = model
        self.launch_date = launch_date
        self.price = price
        self.ground_type = ground_type
        self.material = material
        self.weight = weight
        self.players = players

    def get_brand():
        brand = soup.h2.string.split(" ")[0]
        return brand

    def get_model(self):
        model = soup.h2.string.replace(brand + " ", "")
        return model

    def get_launch_date(self):
        launch_date = soup.find_all('span')[1].string
        return launch_date

    def get_price(self):
        price = list(soup.select('div.detail-title'))[0].p.string
        return price

    def get_ground_type(self):
        if len(list(soup.find_all('ul')[3])) >= 3:
            ground_type = []
            for i in range(1, len(list(soup.find_all('ul')[3]))):
                if i % 2 == 0:
                    pass
                else:
                    ground_type.append(list(soup.find_all('ul')[3])[i].string)
        else:
        	print('no ground type')
        return ground_type

    def get_material(self):
        material = list(soup.select('div.boots-info'))[1].li.string
        return material

    def get_weight(self):
        weight = list(soup.select('div.boots-info'))[2].span.string
        return weight

    def get_players(self):
        if len(list(soup.find_all('ul')[5])) >= 3:
            players = []
            for i in range(1, len(list(soup.find_all('ul')[5]))):
                if i % 2 == 0:
                    pass
                else:
                    players.append(list(soup.find_all('ul')[5])[i].string)
        else:
        	print('no players')
        return players

#debugging
#print('till now we are okay')

i = 1
for i in range(1, 9999):
    print('now...', end="")
    #拼接 url, rnd_referer
    url = 'http://www.footballsilo.com/boots/detail/' + str(i)
    rnd_referer = 'http://www.footballsilo.com/boots/detail/' + str(int(random.uniform(1, 18000)))

    #headers
    headers = {'Host' : 'www.footballsilo.com', 'Connection' : 'keep-alive', 'Cache-Control' : 'max-age=0', 'Upgrade-Insecure-Requests' : '1', 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Referer' : rnd_referer, 'Accept-Encoding' : 'gzip, deflate, sdch', 'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,es;q=0.2,it;q=0.2', 'Cookie' : '_ga=GA1.2.1545417116.1490602283'}
    cookies = {'__cfduid' : 'd0319f0b5d8e088cc7fb6f35201eaec6d1490607492', '_ga' : 'GA1.2.350034646.1490607498'}

    #抓取 HTML
    response = requests.get(url, headers = headers, cookies = cookies)
    print('now we get the response.')
    if response.status_code == 200 and not 'error' in response.text:
        print('we\'re...', end="")
        time.sleep(0.2)
        soup = BeautifulSoup(response.text, "html.parser")
        print('now we get the soup.')

        print('doing...', end="")
    	
        # 抓基本信息
        brand = Info.get_brand()
        print('now we get the brand: ' + brand)
        model = Info.get_model(model)
        print('and we get the model: ' + model)
        model = model.replace('/', ' SLASH ') #just in case
        launch_date = Info.get_launch_date(launch_date)
        print('and we get the launch date: ' + launch_date)
        price = Info.get_price(price)
        print('and we get the price: ' + price)
        ground_type = Info.get_ground_type(ground_type)
        print('and we get the ground type: ' + str(ground_type))
        material = Info.get_material(material)
        print('and we get the material: ' + material)
        weight = Info.get_weight(weight)
        print('and we get the weight: ' + weight)
        players = Info.get_players(players)
        print('and we get the players: ' + str(players))
        #print('now we done the zhuajibenxinxi part.')

        # 抓图片地址
        img_url_group = []
        # no need to sleep here
        #time.sleep(3)
		
        # just in case there's no 'ul.slides'
        #while len(list(soup.select('ul.slides'))[0].contents) > 1:
        for j in range(1, len(list(soup.select('ul.slides'))[0].contents)):
        	if j % 2 == 0:
        		pass
        	else:
        		img_url_group.append(list(soup.select('ul.slides'))[0].contents[j].img['src'])
        print(img_url_group)

        # 建目录
        while not os.path.isdir(brand):
            os.mkdir(brand)
        os.chdir(brand)
        while not os.path.isdir(model):
            os.mkdir(model)
        os.chdir(model)
        print('directories are okay. \n')

        # 存图片
        img_count = 0
        for img_url in img_url_group:
            img = requests.get(img_url, stream=True)
            img_file_name = brand + " " + model + launch_date + "_" + str(img_count) + '.jpg'
            with open(img_file_name, 'wb') as img_file:
                img_file.write(img.content)
            print('.', end="")
            img_count += 1

        # 写 csv
        print('done. \n')
        os.chdir(root_dir)
        f = open('fbsilo.csv', 'a')
        headers = ['Brand', 'Model', 'Launch Date', 'Price', 'Ground Type', 'Material', 'Weight', 'Players']
        #headers = ['Brand', 'Model', 'Launch Date', 'Price', 'Material', 'Weight', 'Players']
    	#f_csv = csv.DictWriter(f, headers)
    	#f_csv.writeheader()
    
        rows_dict = [{'Brand' : brand, 'Model' : model, 'Launch Date': launch_date, 'Price' : price, 'Ground Type' : ground_type, 'Material' : material, 'Weight' : weight, 'Players' : players}]
        #rows_dict = [{'Brand' : brand, 'Model' : model, 'Launch Date': launch_date, 'Price' : price, 'Weight' : weight, 'Players' : players}]
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerows(rows_dict)
        f.close()
        print('csv wrote. \n')

        # 打印
        print("So we now have #" + str(i) + " " + brand + " " + model + " all done." + "\n" + 'img_count: ' + str(img_count) + '\n' + "referer:" + rnd_referer + '\n')

        # 延时
        rnd_time_interval = random.uniform(0.5, 1)
        time.sleep(rnd_time_interval)
    
    else:
        print('blocked by boot #' + str(i) + " . So we happily go for the next." + '\n')
        os.chdir(root_dir)
        #it seems not necessary to sleep for now for here.
        #time.sleep(1)
