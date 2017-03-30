#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 先抓鞋

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
i = 200
for i in range(200, 9999):
    print('now...', end="")
    #拼接 url, rnd_referer
    url = 'http://www.footballbootsdb.com/boot/*/' + str(i)
    rnd_referer = 'http://www.footballbootsdb.com/boot/*/' + str(int(random.uniform(1, 18000)))

    #headers
    headers = {'Host' : 'www.footballbootsdb.com', 'Connection' : 'keep-alive', 'Cache-Control' : 'max-age=0', 'Upgrade-Insecure-Requests' : '1', 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Referer' : rnd_referer, 'Accept-Encoding' : 'gzip, deflate, sdch', 'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,es;q=0.2,it;q=0.2', 'Cookie' : '_ga=GA1.2.1545417116.1490602283'}
    
    #抓取 HTML
    response = requests.get(url, headers = headers, )
    if response.status_code == 200:
        print('we\'re...', end="")
        soup = BeautifulSoup(response.text, "html.parser")
        current_url = soup.head.link['href']

        # detect status code
        if len(soup.h1.string.split(" ")) > 2:

            print('doing...', end="")
        	
            # 抓品牌、系列
            title = list(soup.find_all('h1'))[0].string
            
            if title.split(" ")[0][:3] == 'New':
                brand = brand_list['New']
            elif title.split(" ")[0][:5] == 'Conca':
                brand = brand_list['Conca']
            elif title.split(" ")[0][:5] == 'Conco':
                brand = brand_list['Conco']
            elif title.split(" ")[0][:5] == 'Under':
                brand = brand_list['Und']
            else:
                brand = title.split(" ")[0]
            
            print(brand + '...', end="")
            model = title.replace(brand + " ", "")
            model = model.replace('/', ' SLASH ')
            print(model +'. \n')

            # 抓代言
            players = []
            p = 1
            if 'Popular' in str(soup.h2):
                if len(list(soup.select(".player-list-table"))[0].contents[3].contents) - 1 <= 2:
                    players.append(list(soup.select(".player-list-table"))[0].contents[3].contents[p].contents[5].string)
                    print(players[0] + ' and so on wear ' + brand + ' ' + model + '. \n')
                else:
                    for p in range(1, len(list(soup.select(".player-list-table"))[0].contents[3].contents) - 1):
                        if p % 2 == 0:
                            pass
                        else:
                            players.append(list(soup.select(".player-list-table"))[0].contents[3].contents[p].contents[5].string)
                            print(players[0] + ' and so on wear ' + brand + ' ' + model + '. \n')
            else:
                print('seems like no one wears it...')
            

            # 建目录
            while not os.path.isdir(brand):
                os.mkdir(brand)
            os.chdir(brand)
            while not os.path.isdir(model):
                os.mkdir(model)
            os.chdir(model)
            print('directories are okay. \n')

            # 抓图片地址
            img_url_group = []
            print('getting images.', end="")
            for j in range(0, len(soup.find_all('img'))):
                if 'boots' in list(soup.find_all('img'))[j]['src']:
                    img_url = 'http://www.footballbootsdb.com' + soup.find_all('img')[j]['src']
                    if '?' in img_url:
                        img_url = img_url.replace('?w=250',"")
                    else:
                        pass
                    img_url_group.append(img_url)
                    #debug
                    #print(img_url + ' is added to img_url_group.')
                else:
                    pass

            # 存图片
            for img_url in img_url_group:
                img = requests.get(img_url, stream=True)
                img_file_name = brand + " " + model + "_" + str(k) + '.' + img_url.split('.')[-1]
                k += 1
                with open(img_file_name, 'wb') as img_file:
                    img_file.write(img.content)
                print('.', end="")
                img_count += 1
                #try not to sleep for a while
                #time.sleep(0.5)

        	# 写 csv
            print('done. \n')
            os.chdir(root_dir)
            f = open('fbdb.csv', 'a')
            headers = ['Brand', 'Model', 'Price', 'Players']
        	#f_csv = csv.DictWriter(f, headers)
        	#f_csv.writeheader()
        
            rows_dict = [{'Brand' : brand, 'Model' : model, 'Price' : 0, 'Players' : players}]
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerows(rows_dict)
            f.close()
            print('csv wrote. \n')

            # 打印
            print("So we now have #" + str(i) + " " + brand + " " + model + " all done." + '\n' + current_url + "\n" + "referer:" + rnd_referer + '\n')

            # 延时
            rnd_time_interval = random.uniform(0.1, 1)
            time.sleep(rnd_time_interval)
        
        else:
            print('blocked by boot #' + str(i) + " . So we happily go for the next." + '\n')
            os.chdir(root_dir)
            i = i + 1
            #it seems not necessary to sleep for now for here.
            #time.sleep(0.5)
    else:
        print('404, moving on... \n')