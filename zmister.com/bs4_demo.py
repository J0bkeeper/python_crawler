#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 10:29'


import requests
from bs4 import BeautifulSoup

url = "http://news.qq.com/"

response = requests.get(url).text

soup = BeautifulSoup(response,'lxml')

news_titles = soup.select("div.text a.linkto")

for n in news_titles:
    title = n.get_text()
    link = n.get("href")
    data = {
        '标题':title,
        '链接':link
    }
    print(data)