#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:58:25 2017

@author: romanromanenko
"""
# another easy way of scraping
#import pandas as pd
#
#dfs = pd.read_html('http://cbr.ru/',header=0)
#for df in dfs:
#    print(df, '*******')

# this script gets the main page at cbr.ru, takes the usd and euro currency
# exchange rates and emails them to a certain email

import bs4 as bs
import urllib.request

source = urllib.request.urlopen("http://cbr.ru/").read()
soup = bs.BeautifulSoup(source,'lxml')

#<div class="w_data_wrap">
#<ins class="rubl">руб.</ins>&nbsp;<i class="up" title="+ 0,5539">↑</i>58,3151</div>

#for div in soup.find_all('div', class_='w_data_wrap'):
#    if 'руб' in div.text:
#        print(div.text)

#['\r\n                      Доллар США $\n', '\nруб.\xa057,7612', '\n\nруб.\xa0↑58,3151\n']
#['\r\n                      Евро €\n', '\nруб.\xa067,5344', '\n\nруб.\xa0↑68,3861\n']
            
cbr_output = ''
for table in soup.find_all('table'):
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        if len(td) and ('Доллар' in td[0].text or 'Евро' in td[0].text):
            row = [i.text.strip().replace(u'\xa0', u' ') for i in td]
            cbr_output += ' '.join(row)+'\n'

print(cbr_output)
