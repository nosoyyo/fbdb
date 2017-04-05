#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 实时获取身价封装为函数
# 加入定时模块
# 加入 headers、cookies、referer、关闭连接

import requests
from bs4 import BeautifulSoup
import threading
import time

# 球员列表 pl
player_list = ('roberto', 'iborra', 'gaitan', 'kovacic', 'jovetic', 'umtiti', 'sansone', 'morata', 'piccini')
pl = player_list

# 球员 ID pi
player_id_list = {pl[0] : 17935, pl[1] : 16466, pl[2] : 15095, pl[3] : 16769, pl[4] : 17236, pl[5] : 15101, pl[6] : 15103, pl[7] : 15100, pl[8] : 15971,}
pil = player_id_list

# 球员成本 pc
player_cost = {pl[0] : 25500, pl[1] : 48000, pl[2] : 33500, pl[3] : 30250, pl[4] : 54000, pl[5] : 32750, pl[6] : 40750, pl[7] : 45000, pl[8] : 12000}
pc = player_cost

    # 循环
    i = 0
    for i in range(0, 9):
        #获取 pi
        _pi = str(pil[pl[i]])

        #拼接 url
        url = 'http://www.futbin.com/17/player/' + _pi
        #headers
        headers = {'Host' : 'www.futbin.com', 'Connection' : 'keep-alive', 'Cache-Control' : 'max-age=0', 'Upgrade-Insecure-Requests' : '1', 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Referer' : 'https://www.futbin.com/17/leagues/Legends', 'Accept-Encoding' : 'gzip, deflate, sdch, br', 'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,es;q=0.2,it;q=0.2', 'Cookie' : 'PHPSESSID=ak88ji74deakv5aus67pfb5rg4; gentype=newgen; platform=ps4; 16_field=full_sunny; __cfduid=d7f635baaece73bf1b8bd69c2103449741488253095; xbox=true; ps=true; consoletype=xone; __gads=ID=ef393f4879b78ac2:T=1488270782:S=ALNI_MZRvEAVpZ9K9D-budpzyJBc7nhMgw; cookieconsent_dismissed=yes; lang=en; __token=2998da26f8944aa271d9c27fa4b1308f112d6d69; __tokenId=231017; _ga=GA1.2.279088692.1488253095; sc_is_visitor_unique=rx9767571.1490357253.A13681BA86CB4FBBA57BEC63C5CB60C3.24.18.17.13.11.11.7.5.2'}
        #cookies
        cookies = {'version' : '0', 'name' : '16_field', 'value' : 'full_sunny', 'port' : 'None', 'port_specified' : 'False', 'domain' : 'www.futbin.com', 'domain_specified' : 'False', 'domain_initial_dot' : 'False', 'path' : '/', 'path_specified' : 'True', 'secure' : 'False', 'expires' : '1521463209', 'discard' : 'False', 'comment' : 'None', 'comment_url' : 'None', 'rest' : '', 'rfc2109' : 'False'}

        # 获取实时身价 _ip
        raw_html = requests.get(url, headers = headers, cookies = cookies, ) 
        soup = BeautifulSoup(raw_html.text, "html.parser") #中间件
        pricespan = soup.select('span#xboxlbin') #中间件
        pricespan = str(pricespan) #转换类型为字符串
        instant_price = filter(str.isdigit, pricespan) #剔除非数字字符
        _ip = int(instant_price) #转换数据类型

        #判断涨跌 _cp, 涨幅 _pp
        _cp = current_profit = float(_ip) *0.95 - pc[pl[i]]
        _pp = profit_percentage = float(_cp / pc[pl[i]])
        if _cp > 0:
            print("Now %s worth %d and he is %3.1f%% up⬆") % (pl[i], int(_ip), float(_pp)) + "\n" 
        elif _cp < 0:
            print("Now %s worth %d and he is %3.1f%% down⬇") % (pl[i], int(_ip), float(_pp)) + "\n" 
        else:
            print("%s is still %d, nothing has changed...") % (pl[i], int(_ip)) + "\n" 
        time.sleep(1)
        return

#获取球员姓名
# name = BeautifulSoup(str(soup.select('.header_name')), "html.parser").span.contents[0].strip()
















