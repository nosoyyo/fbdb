#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4

_id = dict()
_id['morata'] = '15100'
_id['umtiti'] = '15101'
_id['kolo'] = '17242'
_id['jorgensen'] = '18045'
_id['sansone'] = '15103'

_bought = dict()
_bought['morata'] = 45000
_bought['kolo'] = 20000
_bought['umtiti'] = 32750
_bought['jorgensen'] = 1
_bought['sansone'] = 40750

# 拼接 url
_url = 'https://www.futbin.com/17/player/' + _id['morata'] 

# 获取 HTML
html = requests.get(_url)

# 提取 HTML 文本生成 soup 中间件
soup = bs4.BeautifulSoup(html.text, "html.parser")

# 提取身价 span 并处理
# pricespan = str(soup.select('span#xboxlbin'))

# 一步到位提取身价
price = filter(str.isdigit, str(soup.select('span#xboxlbin')))

print price