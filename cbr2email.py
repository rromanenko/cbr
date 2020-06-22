#!/usr/bin/env python3

# this script gets the main page at cbr.ru, takes the usd and euro currency
# exchange rates and emails them to a certain email

from cbr_config import *
import bs4 as bs
import smtplib
# import urllib.request
import requests


def send_email(message):
    """ Send an email to details from config file with a passed message """

    server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    server.starttls()

    # Email details in config file
    server.login(from_email, from_email_pass)

    msg = "\r\n".join([
        "From: " + from_email,
        "To: " + to_email,
        "Subject: USD and Euro today",
        "",
        message
        ])

    server.sendmail(from_email, to_email, msg)
    server.quit()


# source = urllib.request.urlopen("http://cbr.ru/").read()
# soup = bs.BeautifulSoup(source,'lxml')

res = requests.get("http://cbr.ru")
cbrPage = bs.BeautifulSoup(res.text, "html.parser")

# finding the table and the table row with this info
# then combining all <td> in a single string
cbr_output = 'Yesterday\tToday\n'
for table in cbrPage.find_all('table'):
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        if td and ('Доллар' in td[0].text or 'Евро' in td[0].text):
            row = [i.text.strip().replace(u'\xa0', u' ') for i in td]
            cbr_output += '\t'.join(row)+'\n'

cbrOutputASCII = cbr_output.encode('ascii', 'ignore').decode('ascii')
# print(cbrOutputASCII)

# send an email with all details
send_email(cbrOutputASCII)
