#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 13:51'


import requests
import json

url = "https://www.toutiao.com/api/pc/focus/"

headers = {
    'Host': "www.toutiao.com",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    'Cookie': "uuid=\"w:d2be5c771bbb4e17b10e6cce22453e2b\"; UM_distinctid=160967955fa10d-0b631012b74b5a8-49566f-1aeaa0-160967955fb160; tt_webid=6504096706215560717; _ga=GA1.2.654790922.1514353025; _gid=GA1.2.493984233.1514353025; tt_webid=6504096706215560717; WEATHER_CITY=%E5%8C%97%E4%BA%AC; CNZZDATA1259612802=989550930-1514349345-%7C1514349345; __tasessionId=xy77peeg11514353045779",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    'Postman-Token': "643d4d75-3e89-9a6c-ec96-d686fea25539"
    }

response = requests.request("GET", url, headers=headers).text

# print(response)

data = json.loads(response)

news = data['data']['pc_feed_focus']

for n in news:
    title = n['title']
    img_url = n['image_url']
    url = n['media_url']
    print(url,title,"http:"+img_url)