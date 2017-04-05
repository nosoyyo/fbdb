# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup

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
    _url = 'http://www.futbin.com/17/player/' + _pi

    # 获取实时身价 _ip
    raw_html = requests.get(_url) 
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

















