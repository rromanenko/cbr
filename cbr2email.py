#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:42:09 2017

@author: romanromanenko
"""

# this script gets the main page at cbr.ru, takes the usd and euro currency
# exchange rates and emails them to a certain email

import bs4 as bs
import urllib.request

#import for SMTP
from cbr_config import *
import smtplib

source = urllib.request.urlopen("http://cbr.ru/").read()
soup = bs.BeautifulSoup(source,'lxml')

# finding the table and the table row with this info
# then combining all <td> in a single string
cbr_output = ''
for table in soup.find_all('table'):
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        if len(td) and ('Доллар' in td[0].text or 'Евро' in td[0].text):
            row = [i.text.strip().replace(u'\xa0', u' ') for i in td]
            cbr_output += ' '.join(row)+'\n'

#print(cbr_output)

# send an email with all details
server = smtplib.SMTP('smtp.gmail.com', 587)
#server.ehlo()
server.starttls()

# Email details in config file

server.login(from_email, from_email_pass)

msg = "\r\n".join([
  "From: " + from_email,
  "To: " + to_email,
  "Subject: USD and Euro today",
  "",
  cbr_output.encode('ascii', 'ignore').decode('ascii')
  ])

server.sendmail(from_email, to_email, msg)

server.quit()