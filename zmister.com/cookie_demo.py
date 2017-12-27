#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 10:42'

import configparser
import requests
from bs4 import BeautifulSoup

import time
import json

CONFIGFILE="cookie.conf"
config=configparser.RawConfigParser()
config.read(CONFIGFILE)
cookie = config.get("ishareread", "cookie.conf")
# print(cookie.conf)

# url = "http://www.ishareread.com/"
#
last = 109
for num in range(1,last+1):
    url = "http://www.ishareread.com/book/booklist.htm?curPage={}&bookclassid=0&subclassid=0".format(num)
    print(url)
    headers = {
        'Host': "www.ishareread.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        'Referer': "https://www.douban.com/group/topic/95019228/",
        'Cookie': cookie,
        'Connection': "keep-alive",
        'Upgrade-Insecure-Requests': "1",
        'Pragma': "no-cache",
        'Cache-Control': "no-cache"
        }

    response = requests.request("POST", url, headers=headers).text

    # print(response.text)

    soup = BeautifulSoup(response,'lxml')

    # #html body div.list_content div.list_content_right div.booklistcontent div.booklist_bookitem
    data_list = soup.select("div.booklistcontent div.booklist_bookitem")

    # print(data)

    for n in data_list:
        title = n.select("a > h2")
        for t in title:
            title = t.get_text()
            # print(title)
        author = n.select("div.author_container")
        for a in author:
            author = a.get_text()
            author_list = author.strip().split("/")
            author = author_list[0]
            press = author_list[1]
            ISDN = author_list[2]
            # print(author)
            # print(author_list)
        summery = n.select("div.summery > p")
        for s in summery:
            summery = s.get_text()
            # print(s)
        link = n.select("a")
        for l in link:
            link = l.get("href")
            link = "http://www.ishareread.com/book/" + link
            # print(link)
        data = {
            '标题':title,
            '作者':author,
            '出版社':press,
            'IDSN':ISDN,
            '链接':link,
            '简介':summery
        }
        print(data)
        f=open("书籍目录.json","a",encoding="utf-8")
        f.write(json.dumps(data,ensure_ascii=False))
        f.close()
    time.sleep(20)

