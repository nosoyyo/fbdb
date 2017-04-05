#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# 随机 referer
# fixed str issue by switched to python 3
# seperater purifier

import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# 处理数字分隔符
def s_purify(s):
    tmp = '';
    for i in range(0, len(s)):
            tmp = tmp + str(s[i]);
    return tmp

# 循环
i = 1

# regular players started from #35
for i in range(48, 18151):
    
    #拼接 url, rnd_referer
    url = 'http://www.futbin.com/17/player/' + str(i)
    rnd_referer = 'https://www.futbin.com/17/player/' + str(int(random.uniform(1, 18000)))

    #headers, cookies
    headers = {'Host' : 'www.futbin.com', 'Connection' : 'keep-alive', 'Cache-Control' : 'max-age=0', 'Upgrade-Insecure-Requests' : '1', 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Referer' : rnd_referer, 'Accept-Encoding' : 'gzip, deflate, sdch, br', 'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,es;q=0.2,it;q=0.2', 'Cookie' : 'PHPSESSID=ak88ji74deakv5aus67pfb5rg4; gentype=newgen; platform=ps4; 16_field=full_sunny; __cfduid=d7f635baaece73bf1b8bd69c2103449741488253095; xbox=true; ps=true; consoletype=xone; __gads=ID=ef393f4879b78ac2:T=1488270782:S=ALNI_MZRvEAVpZ9K9D-budpzyJBc7nhMgw; cookieconsent_dismissed=yes; lang=en; __token=2998da26f8944aa271d9c27fa4b1308f112d6d69; __tokenId=231017; _ga=GA1.2.279088692.1488253095; sc_is_visitor_unique=rx9767571.1490372702.A13681BA86CB4FBBA57BEC63C5CB60C3.26.19.18.14.11.11.7.5.2'}
    cookies = {'16_field' : 'full_sunny ', 'PHPSESSID' : 'ak88ji74deakv5aus67pfb5rg4', '__cfduid' : 'd7f635baaece73bf1b8bd69c2103449741488253095 ', '__gads' : 'ID=ef393f4879b78ac2:T=1488270782:S=ALNI_MZRvEAVpZ9K9D-budpzyJBc7nhMgw ', '__token' : '2998da26f8944aa271d9c27fa4b1308f112d6d69', '__tokenId' : '231017', '_ga' : 'GA1.2.279088692.1488253095', 'consoletype' : 'xone', 'cookieconsent_dismissed' : 'yes', 'gentype' : 'newgen', 'lang' : 'en', 'platform' : 'ps4', 'ps' : 'true', 'sc_is_visitor_unique' : 'rx9767571.1490446108.A13681BA86CB4FBBA57BEC63C5CB60C3.27.20.19.15.12.12.7.5.2   ', 'xbox' : 'true'}
    
    #抓取 HTML
    raw_html = requests.get(url, headers = headers, cookies = cookies, ) 
    soup = BeautifulSoup(raw_html.text, "html.parser")

    # 获取实时身价 _ip
    instant_price = list(filter(str.isdigit, str(soup.select('span#xboxlbin'))))
    _ip = s_purify(instant_price)

    # 获取球员姓名
    player_name = str(BeautifulSoup(str(soup.select('.header_name')), "html.parser").span.contents[0].strip())

    # 获取 rating, position
    rating_list = list(filter(str.isdigit, BeautifulSoup(str(soup.select('.pcdisplay-rat')), "html.parser").contents[1].string))
    rating = str(rating_list[0]) + str(rating_list[1])
    position = BeautifulSoup(str(soup.select('.pcdisplay-pos')), "html.parser").contents[1].string.strip()

    # 获取 games, goals, assists, yellow, red
    games_ps4 = BeautifulSoup(str(soup.select('.pgp_ps4_holder')), "html.parser").contents[1].div.div.next_element.next_element.next_element.next_element
    goals_ps4 = games_ps4.next_element.next_element.next_element.div.next_element.next_element.next_element.next_element
    assists_ps4 = goals_ps4.next_element.next_element.next_element.contents[3].next_element
    yellow_ps4 = assists_ps4.next_element.next_element.next_element.contents[3].next_element
    red_ps4 = yellow_ps4.next_element.next_element.next_element.contents[2].next_element.next_element

    games_xb1 = BeautifulSoup(str(soup.select('.pgp_xb1_holder')), "html.parser").contents[1].div.div.next_element.next_element.next_element.next_element
    goals_xb1 = games_xb1.next_element.next_element.next_element.div.next_element.next_element.next_element.next_element
    assists_xb1 = goals_xb1.next_element.next_element.next_element.contents[3].next_element
    yellow_xb1 = assists_xb1.next_element.next_element.next_element.contents[3].next_element
    red_xb1 = yellow_xb1.next_element.next_element.next_element.contents[2].next_element.next_element

    # separater purifying
    games_list =[games_ps4, games_xb1]
    for i in range(0, len(games_list)):
            games_list[i] = s_purify(list(filter(str.isdigit, games_list[i])))

    # sum
    games = int(games_list[0]) + int(games_list[1])
    
    # 获取 club, nation, league, skills, weak_foot, foot, height, weight, revision, d_workrate, a_workrate, added_on, origin, DOB
    club = soup.th.next_sibling.next_sibling.next_sibling.next_element.next_sibling.contents[3].contents[0].contents[1].next_element
    nation = club.next_element.next_element.next_element.a.next_element
    league = nation.next_element.next_element.next_element.a.next_element
    skills = league.next_element.next_element.next_element.td.next_element
    weak_foot = skills.next_element.next_element.next_element.next_element.td.next_element
    foot = weak_foot.next_element.next_element.next_element.next_element.td.next_element
    height_tmp = foot.next_element.next_element.next_element.td.next_element
    height =  height_tmp[:3]
    weight = height_tmp.next_element.next_element.next_element.td.next_element
    revision = weight.next_element.next_element.next_element.td.next_element
    d_workrate = revision.next_element.next_element.next_element.td.next_element
    a_workrate = d_workrate.next_element.next_element.next_element.td.next_element
    added_on = a_workrate.next_element.next_element.next_element.td.next_element
    origin = added_on.next_element.next_element.next_element.td.next_element
    DOB = str(origin.next_element.next_element.next_element.a)[110:120]

    # 写文件
    f = open('fut17.csv', 'a')
    headers = ['Player Name', 'Instant Price', 'Rating', 'Club', 'Position', 'Nation', 'League', 'Skills', 'Weak Foot', 'Preferred Foot', 'Height', 'Weight', 'Revision', 'Defensive Workrate', 'Attacking Workrate', 'Added On', 'Origin', 'Games PS4', 'Games Xbox 1', 'Total Games', 'Goals Avr. PS4', 'Goals Avr. Xbox 1', 'Assists Avr. PS4', 'Assists Avr. Xbox 1', 'Yellow Avr. PS4', 'Yellow Avr. Xbox 1', 'Red Avr. PS4', 'Red Avr. Xbox 1', 'Date of Birth']
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    
    rows_dict = [{'Player Name' : player_name, 'Instant Price' : str(_ip), 'Rating' : str(rating), 'Club' : str(club), 'Position' : str(position), 'Nation' : str(nation), 'League' : str(league), 'Skills' : str(skills), 'Weak Foot' : str(weak_foot), 'Preferred Foot' : str(foot), 'Height' : str(height), 'Weight' : str(weight), 'Revision' : str(revision), 'Defensive Workrate' : str(d_workrate), 'Attacking Workrate' : str(a_workrate), 'Added On' : str(added_on), 'Origin' : str(origin), 'Games PS4' : str(games_ps4), 'Games Xbox 1' : str(games_xb1), 'Total Games' : str(games), 'Goals Avr. PS4' : str(goals_ps4), 'Goals Avr. Xbox 1' : str(goals_xb1), 'Assists Avr. PS4' : str(assists_ps4), 'Assists Avr. Xbox 1' : str(assists_xb1), 'Yellow Avr. PS4' : str(yellow_ps4), 'Yellow Avr. Xbox 1' : str(yellow_xb1), 'Red Avr. PS4' : str(red_ps4), 'Red Avr. Xbox 1' : str(red_xb1), 'Date of Birth' : str(DOB)}]
    #rows = [player_name, str(_ip), str(rating), str(club), str(position), str(nation), str(league), str(skills), str(weak_foot), str(foot), str(height), str(weight), str(revision), str(d_workrate), str(a_workrate), str(added_on), str(origin), str(games_ps4), str(games_xb1), str(games), str(goals_ps4), str(goals_xb1), str(assists_ps4), str(assists_xb1), str(yellow_ps4), str(yellow_xb1), str(red_ps4), str(red_xb1), str(DOB)]
    f_csv.writerows(rows_dict)
    f.close()

    # 打印
    print("We've got " + player_name + " done." + '\n' + url + "\n" + "referer:" + rnd_referer + '\n')

    # 延时
    rnd_time_interval = random.uniform(10, 20)
    time.sleep(rnd_time_interval)
    


















