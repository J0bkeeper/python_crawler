#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.28 08:48'

import requests
import json
import pymongo

# 链接MongoDB
conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
toutiaohao = conn['toutiaohao']
news = toutiaohao['news']

headers = {
    'Host': 'www.toutiao.com',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
    'Connection': 'Keep-Alive',
    'Content-Type': 'text/plain; Charset=UTF-8',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn',
    'Cookie': '__tasessionId=x57suhyhv1500091331200;cp=5969D943FCF37E1',
}


def scrap_toutiao(uid):
    url = 'http://www.toutiao.com/c/user/article/?page_type=1&user_id={uid}&max_behot_time=0&count=60&as=A175F9F659893C3&cp=5969D943FCF37E1'.format(
        uid=uid)
    response = requests.get(url, headers=headers).text
    data = json.loads(response, encoding='utf-8')['data']
    if len(data) != 0:
        for d in data:
            try:
                category = d['chinese_tag']
            except:
                category = '其他'
            result = {
                'title': d['title'],
                'readcount': d['go_detail_count'],
                'category': category,
                'comment': d['comments_count'],
                'author': d['source']
            }
            print(result)
            news.insert_one(result)


with open('今日头条ID.txt', mode='r') as text:
    oneid = text.readlines()
    for i in oneid:
        print(i, end='')
        scrap_toutiao(uid=i)

conn.close()
