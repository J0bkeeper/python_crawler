#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.28 13:33'


import requests
from bs4 import BeautifulSoup


url = "http://music.baidu.com/songlist"

headers = {
    'Host': "music.baidu.com",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    'Referer': "https://www.baidu.com/link?url=YRMJtp1q4mlfXNSgy7qKaLbrGDermIoYTQJdt8mYMrFJ38cUE7ws-ADiQDMs4wxb&wd=&eqid=a39bf9c30004b501000000035a44813f",
    'Cookie': "BAIDUID=565B8993B043C541FBC55CD6459D04CE:FG=1; BIDUPSID=565B8993B043C541FBC55CD6459D04CE; PSTM=1507850643; FP_UID=54eed2e0cc74b9d098c40306725f4b64; H_PS_PSSID=1431_21120_25439_25178; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[Fc9oatPmwxn]=srT4swvGNE6uzdhUL68mv3; tracesrc=-1%7C%7Cwww.baidu.com; u_lo=0; u_id=; u_t=; app_vip=show",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    }

response = requests.request("GET", url, headers=headers).text

# print(response.text)

soup = BeautifulSoup(response,'lxml')

song_list = soup.select("div.songlist-list > ul")

for song in song_list:
    titles = song.select("li p.text-title a")
    for title in titles:
        print(title.get_text())