#!/usr/bin/env python
# -*- coding: utf-8 -*-

# new in 0.3: random referer in headers
# fixed in 0.3: fixed str issue by switched to python 3
# new in 0.31: added seperater purifier
# new in 0.4: added changelog
# new in 0.4: added origin sniffer
# <del>tbf: fuck csv especially the fucking headers issue</del>
# fixed in 0.4: fucking csv issues
# fixed in 0.5: when a certain number of url token doesn't contain a player
# new in 0.6: reconstruction
# new in 0.6: get full name
# new in 0.6: get full attributes
# new in 0.6: url token as order in csv
# new in 0.6: starting time, total time, and some analytics
# new in 0.7: added gc.collect()

# new in 0.8: roughly set up for FIFA18
# tbd/new in 0.8: optimized with goalkeepers
# new in 0.8: deal with players w/ or wo/ intl_rep

# new in 0.9: AJAX, json & MongoDB
# new in 0.91: GUI, 1hr snap, update if player exists 

# tbd: counter of done works
# tbd: wechat me for any news good or bad
# tbd: email me when break

# tbd: 1.0, fully functional and automatic

__author__ = 'nosoyyo'
import requests
from bs4 import BeautifulSoup
import gc
import csv
import json
import timeit
import random
import pymongo

# collect numbers within string
def onlyNum(s):
    tmp = '';
    for i in range(0, len(s)):
        if str(s[i]).isdigit():
            tmp = tmp + str(s[i]);
        else:
            pass
    return tmp

started_at = timeit.default_timer()
n_items = 1
duration = 0

# main

for i in range(5020, 16010):

    #拼接 url, rnd_referer
    url = 'http://www.futbin.com/18/player/' + str(i)
    rnd_referer = 'https://www.futbin.com/18/player/' + str(int(random.uniform(1, 16000)))

    #headers, cookies
    # take a snap every 1hr
    if duration % 60 > 55:
#            rnd_time_interval = random.uniform(0.5, 1)
        time.sleep(600)
        #add connection close into headers
        headers = {"Connection" : "close", 'accept' : 'text/html', 'accept-encoding' : 'gzip', 'cache-control' : 'max-age=0', 'cookie' : 'PHPSESSID=8352d14773681915ba9f9fca29404062; platform=ps4; _ga=GA1.2.1931620846.1515132876; _gid=GA1.2.193899811.1515132876; xbox=true; ps=true; pc=true; OX_plg=pm; __gads=ID=17b3c1a533b9ce27:T=1515132916:S=ALNI_MbkNMV175g7e6ObdaLnT6HhZFUZDw; _dm_sync=true; cookieconsent_dismissed=yes; OX_sd=8; sc_is_visitor_unique=rx9767571.1515140976.7158A1C2145D4F80CD39A3074984500A.2.2.1.1.1.1.1.1.1', 'upgrade-insecure-requests' : '1', 'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', "Referer" : rnd_referer}
    else:
        headers = {'accept' : 'text/html', 'accept-encoding' : 'gzip', 'cache-control' : 'max-age=0', 'cookie' : 'PHPSESSID=8352d14773681915ba9f9fca29404062; platform=ps4; _ga=GA1.2.1931620846.1515132876; _gid=GA1.2.193899811.1515132876; xbox=true; ps=true; pc=true; OX_plg=pm; __gads=ID=17b3c1a533b9ce27:T=1515132916:S=ALNI_MbkNMV175g7e6ObdaLnT6HhZFUZDw; _dm_sync=true; cookieconsent_dismissed=yes; OX_sd=8; sc_is_visitor_unique=rx9767571.1515140976.7158A1C2145D4F80CD39A3074984500A.2.2.1.1.1.1.1.1.1', 'upgrade-insecure-requests' : '1', 'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', "Referer" : rnd_referer}
    
    cookies = {'16_field' : 'full_sunny ', '__cfduid' : 'd7f635baaece73bf1b8bd69c2103449741488253095 ', '__gads' : 'ID=ef393f4879b78ac2:T=1488270782:S=ALNI_MZRvEAVpZ9K9D-budpzyJBc7nhMgw ', '__token' : '2998da26f8944aa271d9c27fa4b1308f112d6d69', '__tokenId' : '231017', '_ga' : 'GA1.2.279088692.1488253095', 'consoletype' : 'xone', 'cookieconsent_dismissed' : 'yes', 'gentype' : 'newgen', 'lang' : 'en', 'platform' : 'ps4', 'ps' : 'true', 'sc_is_visitor_unique' : 'rx9767571.1490446108.A13681BA86CB4FBBA57BEC63C5CB60C3.27.20.19.15.12.12.7.5.2   ', 'xbox' : 'true'}

    #get the html, get it souped
    response = requests.get(url, headers = headers, cookies = cookies, )
    soup = BeautifulSoup(response.text, "html.parser")

    #get player_resource_id for XHR 
    prid = soup.select('div#page-info')[0].attrs['data-player-resource']

    # normal len(soup) == 68, 404 len(soup) == 10
    if len(soup) > 10:
    
        url_token = url.split('/')[-1]
        player_name = soup.select('span.header_name')[0].string
        full_name = soup.title.string.split(" - ")[1][:-9]
        rating = soup.find_all(attrs={"class" : "pcdisplay-rat"})[0].string

        z = list(soup.find_all('td','table-row-text'))

        club = z[1].a.string 
        position = soup.find_all(attrs={"class" : "pcdisplay-pos"})[0].string.strip() 
        nation = z[2].a.string 
        league = z[3].a.string 
        skills = z[4].next_element
        weak_foot = z[5].next_element

        # check if intl_rep exists
        if "Intl. Rep" in soup.select("div#info_content")[0].text: 
            intl_rep = z[6].text.strip()
            foot = z[7].string.strip()
            height = z[8].string[:3] 
            weight = z[9].string.strip()
            revision = z[10].string
            d_workrate = z[11].string
            a_workrate = z[12].string
            added_on = z[13].string
            if len(list(z[14])) > 2:
                origin = z[14].a.string.strip()
            else:
                origin = z[14].string.strip()
            DOB = str(z[15])[138:148]
        else: 
            intl_rep = "N/A"
            foot = z[6].text.strip()
            height = z[7].string[:3]
            weight = z[8].string.strip()
            revision = z[9].string
            d_workrate = z[10].string
            a_workrate = z[11].string
            added_on = z[12].string
            if len(list(z[13])) > 2:
                origin = z[13].a.string.strip()
            else:
                origin = z[13].string.strip()
            DOB = str(z[14])[138:148]

        info_ps4 = soup.find_all(attrs={"class" : "ps4-pgp-data"})
        games_ps4 = info_ps4[5].string.strip()
        goals_ps4 = info_ps4[4].string.strip()
        assists_ps4 = info_ps4[3].string.strip()
        yellow_ps4 = info_ps4[2].string.strip()
        red_ps4 = info_ps4[1].string.strip()
        top_chem_ps4 = list(info_ps4[0])[1].text.strip()

        info_xb1 = soup.find_all(attrs={"class" : "xbox-pgp-data"})
        games_xb1 = info_xb1[5].string.strip()
        goals_xb1 = info_xb1[4].string.strip()
        assists_xb1 = info_xb1[3].string.strip()
        yellow_xb1 = info_xb1[2].string.strip()
        red_xb1 =  info_xb1[1].string.strip()
        top_chem_xb1 = list(info_xb1[0])[1].text.strip()

        # separater purifying, games summing up
        games_list =[games_ps4, games_xb1]
        if not games_ps4 and games_xb1 == 0:
            for ii in range(0, len(games_list)):
                games_list[ii] = onlyNum(list(filter(str.isdigit, games_list[ii])))
            total_games = int(games_list[0]) + int(games_list[1])
        elif games_ps4 == 0:
            total_games = games_xb1
        elif games_xb1 == 0:
            total_games = games_ps4
        else:    
            total_games = 0

        # get player attributes json
        pajson = soup.select('div#player_stats_json')


        # update'em in MongoDB
        client = pymongo.MongoClient("localhost", 27017)
        db = client.fut18
        players = db["players"]
        # check if player alerady exists
        if full_name in str(players.find_one({"full_name" : full_name})):
            players.update({"full_name": full_name}, {"$set":{'player_name' : player_name, 'rating' : rating, 'club' : club, 'position' : position, 'nation' : nation, 'league' : league, 'skills' : skills, 'weak_foot' : weak_foot, 'intl_rep' : intl_rep, 'foot' : foot, 'height' : height, 'weight' : weight, 'revision' : revision, 'd_workrate' : d_workrate, 'a_workrate' : a_workrate, 'added_on' : added_on, 'games_ps4' : games_ps4, 'games_xb1' : games_xb1, 'total_games' : total_games}})
        else:
            player = {'player_name' : player_name, 'full_name' : full_name, 'rating' : rating, 'club' : club, 'position' : position, 'nation' : nation, 'league' : league, 'skills' : skills, 'weak_foot' : weak_foot, 'intl_rep' : intl_rep, 'foot' : foot, 'height' : height, 'weight' : weight, 'revision' : revision, 'd_workrate' : d_workrate, 'a_workrate' : a_workrate, 'added_on' : added_on, 'games_ps4' : games_ps4, 'games_xb1' : games_xb1, 'total_games' : total_games}
            players.insert(player)

        # 打印 + 状态 + 分析
        duration = (timeit.default_timer() - started_at) / 60
        avr_players = n_items / float(duration)

        #GUI
        print("""┌──────────────────────────────────────────────────────────────────────────────┐""")
        print("""│                                                                              │""")
        print("""│                 ___          __       _     __                               │""")
        print("""│               /'___\        /\ \__  /' \  /'_ `\                             │""")
        print("""│              /\ \__/  __  __\ \ ,_\/\_, \/\ \L\ \                  fut       │""")
        print("""│              \ \ ,__\/\ \/\ \\ \ \/\/_/\ \/_> _ <_                  18        │""")
        print("""│               \ \ \_/\ \ \_\ \\ \ \_  \ \ \/\ \L\ \                           │""")
        print("""│                \ \_\  \ \____/ \ \__\  \ \_\ \____/              nosoyyo     │""")
        print("""│                 \/_/   \/___/   \/__/   \/_/\/___/                           │""")
        print("""│                                                                              │""")
        print("""│                                                                              │""")
        print("""│                                                                              │""")
        print("""│                                                                              │""")

        # auto-center-align
        print("│                                  We've got                                   │")
        player_done = "#" + str(url_token) + " " + player_name + " done."
        acl = round((78 - len(player_done)) / 2)
        acr = 78 - len(player_done) - acl
        print("│" + " " * acl + player_done + " " * acr + "│")
        acl = round((78 - len(url)) /2)
        acr = 78 - len(url) - acl
        print("│" + " " * acl + url + " " * acr + "│")
        acl = round((78 - len("Referer: " + rnd_referer)) /2)
        acr = 78 - len("Referer: " + rnd_referer) - acl
        print("│" + " " * acl + "Referer: " + rnd_referer + " " * acr + "│")
        print("""│                                                                              │""")
        print("""│                                                                              │""")
        print("├──────────────────────────────────────────────────────────────────────────────┤")

        # simple stats
        print('│ Total ' + str(n_items) + ' players in ' + str(round(duration, 2)) + ' mins. ' + str(round(avr_players, 2)) + ' plrs/min avr.')
        percentage = round(int(url_token) / 16010 * 100, 2)
        print('│ ' + str(percentage) + '%')
        print("└──────────────────────────────────────────────────────────────────────────────┘")

        n_items += 1

        # A best guess
        gc.collect()

    else:
        print('Player #' + str(i) + " doesn't exist. Now we go for the next." + '\n')
        i = i + 1
