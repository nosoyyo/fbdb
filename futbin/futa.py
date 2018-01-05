#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

big_league = ['LaLiga Santander ', 'Premier League', 'Calcio A', 'Bundesliga', 'Ligue 1']

# read file.
df = pd.read_csv('fut17_full.csv')

# some naive analytics.
full_name_list = list(frob.iloc[:,3])
len(set(df.iloc[:,3])) # 14552

# Gold millionaires.
# set(df[(df.iloc[:,22] > 999999) & (df.iloc[:,4] > 75)].iloc[:,3]) # 215
# df[(df.iloc[:,22] > 999999) & (df.iloc[:,4] > 75) & (df.iloc[:,8].values in big_league)].iloc[:,3]
# (Surprisingly) All millionaires are gold.
set(df[(df.iloc[:,22] > 999999)].iloc[:,3]) # 215
min(df[df.iloc[:,22] > 999999].iloc[:,4]) # 76, the lowest rating of a millionaire

for i in range(0,216):
    print(df[(df.iloc[:,22] > 999999)].iloc[:,3].values[i] + ' ' + df[(df.iloc[:,22] > 999999)].iloc[:,8].values[i])

m = df[(df.iloc[:,22] > 999999)]

# set(df[(df.iloc[:,6] == 'GK')].iloc[:,3]) # 1635
set(df[(df.iloc[:,6] == 'GK') & (df.iloc[:,12] < 180)].iloc[:,3]) # 27
set(df[(df.iloc[:,6] == 'GK') & (df.iloc[:,12] < 185) & (df.iloc[:,12] >= 180)].iloc[:,3]) # 294
set(df[(df.iloc[:,6] == 'GK') & (df.iloc[:,12] < 190) & (df.iloc[:,12] >= 185)].iloc[:,3]) # 677
set(df[(df.iloc[:,6] == 'GK') & (df.iloc[:,12] < 195) & (df.iloc[:,12] >= 190)].iloc[:,3]) # 494
set(df[(df.iloc[:,6] == 'GK') & (df.iloc[:,12] < 200) & (df.iloc[:,12] >= 195)].iloc[:,3]) # 134
set(df[(df.iloc[:,6] == 'GK') & (df.iloc[:,12] >= 200)].iloc[:,3]) # 10

#skills and weak_foot analytics
set(df[(df.iloc[:,9] == 5) & (df.iloc[:,10] == 5)].iloc[:,3]) # Only Neymar and Musonda
set(df[(df.iloc[:,9] == 4) & (df.iloc[:,10] == 5)].iloc[:,3]) # 35
set(df[(df.iloc[:,9] == 5) & (df.iloc[:,10] == 4)].iloc[:,3]) # 20

#workrate analytics
set(df[(df.iloc[:,15] == 'High') & (df.iloc[:,16] == 'High')].iloc[:,3]) # 662
