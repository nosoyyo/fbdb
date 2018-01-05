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

# tbd: counter of done works
# tbd: wechat me for any news good or bad
# tbd: email me when break
# tbd: randomly scrap a player from pool

__author__ = 'nosoyyo'
import requests
from bs4 import BeautifulSoup
import gc
import csv
import time
import random

#dealing with separaters
def s_purify(s):
    tmp = '';
    for i in range(0, len(s)):
            tmp = tmp + str(s[i]);
    return tmp

starting_time = time.time()
n_items = 1

# 循环

for i in range(33855, 40000):

    #拼接 url, rnd_referer
    url = 'http://www.futbin.com/16/player/' + str(i)
    rnd_referer = 'https://www.futbin.com/16/player/' + str(int(random.uniform(1, 18000)))

    #headers, cookies
    headers = {'Host' : 'www.futbin.com', 'Connection' : 'keep-alive', 'Cache-Control' : 'max-age=0', 'Upgrade-Insecure-Requests' : '1', 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Referer' : rnd_referer, 'Accept-Encoding' : 'gzip, deflate, sdch, br', 'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,es;q=0.2,it;q=0.2', 'Cookie' : 'PHPSESSID=ak88ji74deakv5aus67pfb5rg4; gentype=newgen; platform=ps4; 16_field=full_sunny; __cfduid=d7f635baaece73bf1b8bd69c2103449741488253095; xbox=true; ps=true; consoletype=xone; __gads=ID=ef393f4879b78ac2:T=1488270782:S=ALNI_MZRvEAVpZ9K9D-budpzyJBc7nhMgw; cookieconsent_dismissed=yes; lang=en; __token=2998da26f8944aa271d9c27fa4b1308f112d6d69; __tokenId=231017; _ga=GA1.2.279088692.1488253095; sc_is_visitor_unique=rx9767571.1490372702.A13681BA86CB4FBBA57BEC63C5CB60C3.26.19.18.14.11.11.7.5.2'}
    cookies = {'16_field' : 'full_sunny ', 'PHPSESSID' : 'ak88ji74deakv5aus67pfb5rg4', '__cfduid' : 'd7f635baaece73bf1b8bd69c2103449741488253095 ', '__gads' : 'ID=ef393f4879b78ac2:T=1488270782:S=ALNI_MZRvEAVpZ9K9D-budpzyJBc7nhMgw ', '__token' : '2998da26f8944aa271d9c27fa4b1308f112d6d69', '__tokenId' : '231017', '_ga' : 'GA1.2.279088692.1488253095', 'consoletype' : 'xone', 'cookieconsent_dismissed' : 'yes', 'gentype' : 'newgen', 'lang' : 'en', 'platform' : 'ps4', 'ps' : 'true', 'sc_is_visitor_unique' : 'rx9767571.1490446108.A13681BA86CB4FBBA57BEC63C5CB60C3.27.20.19.15.12.12.7.5.2   ', 'xbox' : 'true'}

    #抓取 HTML
    response = requests.get(url, headers = headers, cookies = cookies, )
    soup = BeautifulSoup(response.text, "html.parser")

    # normal len(soup) == 68, 404 len(soup) == 10
    if len(soup) > 10:
        #fieldnames[:5]
        url_token = url.split('/')[-1]
        player_name = soup.select('span.header_name')[0].string
        instant_price = s_purify(list(filter(str.isdigit, str(soup.select('span#xboxlbin')))))
        full_name = soup.title.string.split(" - ")[1][:-3]
        rating = soup.title.string.split(" - ")[1][-2:]

        # fieldnames[5:20]
        z = list(soup.find_all('td','table-row-text'))

        club = z[1].a.string # fieldnames[5]
        position = soup.find_all(attrs={"class" : "pcdisplay-pos"})[0].string.strip() # fieldnames[6]
        nation = z[2].a.string # fieldnames[7]
        league = z[3].a.string # fieldnames[8]
        skills = z[4].next_element # fieldnames[9]
        weak_foot = z[5].next_element # fieldnames[10]
        foot = z[6].string # fieldnames[11]
        height = z[7].string[:3] # fieldnames[12]
        weight = z[8].string # fieldnames[13]
        revision = z[9].string # fieldnames[14]
        d_workrate = z[10].string # fieldnames[15]
        a_workrate = z[11].string # fieldnames[16]
        added_on = z[12].string # fieldnames[17]
        if len(list(z[13])) > 2:
            origin = z[13].a.string.strip()
        else:
            origin = z[13].string.strip()
        DOB = str(z[14])[138:148] # fieldnames[19]

        # fieldnames[20:31]
#        h_ps4 = soup.find_all(attrs={"class" : "pgp_ps4_holder"})[0].contents
#        for item in h_ps4:
#            h_ps4.remove('\n')
#        games_ps4 = h_ps4[0].contents[3].string # fieldnames[20]
#        goals_ps4 = h_ps4[1].contents[3].string # fieldnames[23]
#        assists_ps4 = h_ps4[2].contents[3].string # fieldnames[25]
#        yellow_ps4 = h_ps4[3].contents[3].string # fieldnames[27]
#        red_ps4 = h_ps4[4].contents[3].string # fieldnames[29]

#        h_xb1 = soup.find_all(attrs={"class" : "pgp_xb1_holder"})[0].contents
#        for item in h_xb1:
#            h_xb1.remove('\n')
#        games_xb1 = h_xb1[0].contents[3].string # fieldnames[21]
#        goals_xb1 = h_xb1[1].contents[3].string # fieldnames[24]
#        assists_xb1 = h_xb1[2].contents[3].string # fieldnames[26]
#        yellow_xb1 = h_xb1[3].contents[3].string # fieldnames[28]
#        red_xb1 = h_xb1[4].contents[3].string # fieldnames[30]

        # separater purifying
#        games_list =[games_ps4, games_xb1]
#        for ii in range(0, len(games_list)):
#                games_list[ii] = s_purify(list(filter(str.isdigit, games_list[ii])))

        # sum
#        total_games = int(games_list[0]) + int(games_list[1]) # fieldnames[22]

        # get full_attributes, fieldnames[31:65]
        fa_soup = soup.select('span.statlabel')
        fa_list = []
        for i in range(0, 34):
            fa_list.append(fa_soup[i].string)

        # extract general_attributes
        general_attributes = {'Pace' : fa_list[0], 'Shooting' : fa_list[3], 'Dribbling' : fa_list[10], 'Defending' : fa_list[16], 'Passing' : fa_list[22], 'Physicality' : fa_list[29]}

        # extract detailed attributes
        pace = {'Acceleration' : fa_list[1], 'Sprint Speed' : fa_list[2]}
        shooting_list = {'Positioning' : '', 'Finishing' : '', 'Shot Power' : '', 'Long Shots' : '', 'Volleys' : '', 'Penalties' : ''}
        l = 4
        for key in shooting_list:
            shooting_list[key] = fa_list[l]
            l += 1

        l += 1 # now l == 11
        dribbling_list = {'Agility' : '', 'Balance' : '', 'Reactions' : '', 'Ball control' : '', 'Dribbling' : ''}
        for key in dribbling_list:
            dribbling_list[key] = fa_list[l]
            l += 1

        l += 1 # now l == 17
        defending_list = {'Interceptions' : '', 'Heading Accuracy' : '', 'Marking' : '', 'Standing Tackle' : '', 'Sliding Tackle' : ''}
        for key in defending_list:
            defending_list[key] = fa_list[l]
            l += 1

        l += 1 # now l == 23
        passing_list = {'Vision' : '', 'Crossing' : '', 'FK Accuracy' : '', 'Short Passing' : '', 'Long Passing' : '', 'Curve' : ''}
        for key in passing_list:
            passing_list[key] = fa_list[l]
            l += 1

        l += 1 # now l == 30
        physicality_list = {'Jumping' : '', 'Stamina' : '', 'Strength' : '', 'Aggression' : ''}
        for key in physicality_list:
            physicality_list[key] = fa_list[l]
            l += 1

        # get traits, fieldnames[65:67]
        t_soup = soup.select('div#traits_content')[0].contents
        if 'None' in str(t_soup):
            n_traits = 0
            traits_list = []
        else:
            n_traits = int(len(t_soup) / 2)
            traits_list = []
            t = 1
            for t in range (1, len(t_soup)):
                if t % 2 == 0:
                    pass
                else:
                    traits_list.append(t_soup[t].contents[-1].strip())

        # get specialities, fieldnames[67:69]
        sp_soup = soup.select('div#specialities_content')[0].contents
        if 'None' in str(sp_soup):
            n_specialities = 0
            specialities_list = []
        else:
            n_specialities = int(len(sp_soup) / 2) # fieldnames[67]
            specialities_list = []
            t = 1
            for t in range (1, len(sp_soup)):
                if t % 2 == 0:
                    pass
                else:
                    specialities_list.append(sp_soup[t].contents[-1].strip())

        # 写文件
        f = open('fut16_full.csv', 'a')
        fieldnames = ['url_token', 'Player Name', 'Instant Price', 'Full Name', 'Rating', 'Club', 'Position', 'Nation', 'League', 'Skills', 'Weak Foot', 'Preferred Foot', 'Height', 'Weight', 'Revision', 'Defensive Workrate', 'Attacking Workrate', 'Added On', 'Origin', 'Date of Birth', 'Games PS4', 'Games Xbox 1', 'Total Games', 'Goals Avr. PS4', 'Goals Avr. Xbox 1', 'Assists Avr. PS4', 'Assists Avr. Xbox 1', 'Yellow Avr. PS4', 'Yellow Avr. Xbox 1', 'Red Avr. PS4', 'Red Avr. Xbox 1', 'Pace', 'Acceleration',  'Sprint Speed', 'Shooting', 'Positioning', 'Finishing', 'Shot Power', 'Long Shots', 'Volleys', 'Penalties', 'Dribbling', 'Agility', 'Balance', 'Reactions', 'Ball control', 'Dribbling', 'Defending', 'Interceptions', 'Heading Accuracy', 'Marking', 'Standing Tackle', 'Sliding Tackle', 'Passing', 'Vision', 'Crossing', 'FK Accuracy', 'Short Passing', 'Long Passing', 'Curve', 'Physicality', 'Jumping', 'Stamina', 'Strength', 'Aggression', 'n_traits', 'Traits', 'n_specialities', 'Specialities',]
        # writeheader
        # f_csv = csv.DictWriter(f, fieldnames)
        # f_csv.writeheader()

        rows_dict = [{'url_token': url_token, 'Player Name' : player_name, 'Instant Price' : str(instant_price),'Full Name' : str(full_name), 'Rating' : str(rating), 'Club' : str(club), 'Position' : str(position), 'Nation' : str(nation), 'League' : str(league), 'Skills' : str(skills), 'Weak Foot' : str(weak_foot), 'Preferred Foot' : str(foot), 'Height' : str(height), 'Weight' : str(weight), 'Revision' : str(revision), 'Defensive Workrate' : str(d_workrate), 'Attacking Workrate' : str(a_workrate), 'Added On' : str(added_on), 'Origin' : str(origin), 'Date of Birth' : str(DOB), 'Pace' : general_attributes['Pace'], 'Acceleration' : pace['Acceleration'],  'Sprint Speed' : pace['Sprint Speed'], 'Shooting' : general_attributes['Shooting'], 'Positioning' : shooting_list['Positioning'], 'Finishing' : shooting_list['Finishing'], 'Shot Power' : shooting_list['Shot Power'], 'Long Shots' : shooting_list['Long Shots'], 'Volleys' : shooting_list['Volleys'], 'Penalties' : shooting_list['Penalties'], 'Dribbling' : general_attributes['Dribbling'], 'Agility' : dribbling_list['Agility'], 'Balance' : dribbling_list['Balance'], 'Reactions' : dribbling_list['Reactions'], 'Ball control' : dribbling_list['Ball control'], 'Dribbling' : dribbling_list['Dribbling'], 'Defending' : general_attributes['Defending'], 'Interceptions' : defending_list['Interceptions'], 'Heading Accuracy' : defending_list['Heading Accuracy'], 'Marking' : defending_list['Marking'], 'Standing Tackle' : defending_list['Standing Tackle'], 'Sliding Tackle': defending_list['Sliding Tackle'], 'Passing' : general_attributes['Passing'], 'Vision' : passing_list['Vision'], 'Crossing' : passing_list['Crossing'], 'FK Accuracy' : passing_list['FK Accuracy'], 'Short Passing' : passing_list['Short Passing'], 'Long Passing' : passing_list['Long Passing'], 'Curve' : passing_list['Curve'], 'Physicality' : general_attributes['Physicality'], 'Jumping' : physicality_list['Jumping'], 'Stamina' : physicality_list['Stamina'], 'Strength' : physicality_list['Strength'], 'Aggression' : physicality_list['Aggression'], 'n_traits' : n_traits, 'Traits' : traits_list, 'n_specialities' : n_specialities, 'Specialities' : specialities_list,}]
        #rows = [player_name, str(instant_price), str(rating), str(club), str(position), str(nation), str(league), str(skills), str(weak_foot), str(foot), str(height), str(weight), str(revision), str(d_workrate), str(a_workrate), str(added_on), str(origin), str(games_ps4), str(games_xb1), str(games), str(goals_ps4), str(goals_xb1), str(assists_ps4), str(assists_xb1), str(yellow_ps4), str(yellow_xb1), str(red_ps4), str(red_xb1), str(DOB)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(rows_dict)
        f.close()

        # 打印 + 状态 + 分析
        running_time = (time.time() - starting_time) / 60
        avr_players = n_items / float(running_time)
        print("We've got #" + str(url_token) + " " + player_name + " done." + '\n' + url + "\n" + "referer:" + rnd_referer + '\n')
        print('Total ' + str(n_items) + ' players in ' + str(running_time) + ' mins. ' + str(avr_players) + ' plrs/min avr.')
        n_items += 1

        # It seems it's always around 10 requests/min.
        rnd_time_interval = random.uniform(0.5, 1)
        time.sleep(rnd_time_interval)

        # A best guess
        gc.collect()

    else:
        print('Player #' + str(i) + " doesn't exist. Now we go for the next." + '\n')
        i = i + 1
