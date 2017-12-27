#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 14:31'


import requests
from bs4 import BeautifulSoup
import re

"""
查询要爬取的页面数量
"""

url = "http://sou.zhaopin.com/jobs/searchresult.ashx"

page_num = 1

querystring = {"jl":"%e5%8c%97%e4%ba%ac","kw":"python","sm":"0","sg":"2d8d7bd1731e4c06a4fbbb6aa50d7eb6","p":page_num}

headers = {
    'Host': "sou.zhaopin.com",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    'Referer': "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%e5%8c%97%e4%ba%ac&kw=python&sm=0&sg=2d8d7bd1731e4c06a4fbbb6aa50d7eb6&p=25",
    'Cookie': "urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; dywea=95841923.1156796494429583000.1514356013.1514356013.1514356013.1; dyweb=95841923.16.9.1514356017073; dywec=95841923; dywez=95841923.1514356013.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; _jzqa=1.374266413526592830.1514356013.1514356013.1514356013.1; _jzqb=1.15.10.1514356013.1; _jzqc=1; _jzqckmp=1; _qzja=1.510276591.1514356013020.1514356013020.1514356013020.1514356131746.1514356135102.0.0.0.14.1; _qzjb=1.1514356013020.14.0.0.0; _qzjc=1; _qzjto=14.1.0; __utma=269921210.1726821062.1514356015.1514356015.1514356015.1; __utmb=269921210.16.9.1514356017075; __utmc=269921210; __utmz=269921210.1514356015.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; JSSearchModel=0; LastCity%5Fid=530; LastCity=%e5%8c%97%e4%ba%ac; LastJobTag=%e4%ba%94%e9%99%a9%e4%b8%80%e9%87%91%7c%e5%b8%a6%e8%96%aa%e5%b9%b4%e5%81%87%7c%e8%8a%82%e6%97%a5%e7%a6%8f%e5%88%a9%7c%e7%bb%a9%e6%95%88%e5%a5%96%e9%87%91%7c%e9%a4%90%e8%a1%a5%7c%e5%ae%9a%e6%9c%9f%e4%bd%93%e6%a3%80%7c%e5%bc%b9%e6%80%a7%e5%b7%a5%e4%bd%9c%7c%e8%a1%a5%e5%85%85%e5%8c%bb%e7%96%97%e4%bf%9d%e9%99%a9%7c%e5%b9%b4%e5%ba%95%e5%8f%8c%e8%96%aa%7c%e5%91%98%e5%b7%a5%e6%97%85%e6%b8%b8%7c%e4%ba%a4%e9%80%9a%e8%a1%a5%e5%8a%a9%7c%e9%80%9a%e8%ae%af%e8%a1%a5%e8%b4%b4%7c%e5%8a%a0%e7%8f%ad%e8%a1%a5%e5%8a%a9%7c%e8%82%a1%e7%a5%a8%e6%9c%9f%e6%9d%83%7c%e5%85%8d%e8%b4%b9%e7%8f%ad%e8%bd%a6%7c%e5%85%a8%e5%8b%a4%e5%a5%96%7c%e5%b9%b4%e7%bb%88%e5%88%86%e7%ba%a2%7c%e5%88%9b%e4%b8%9a%e5%85%ac%e5%8f%b8%7c%e5%8c%85%e5%90%83%7c%e6%af%8f%e5%b9%b4%e5%a4%9a%e6%ac%a1%e8%b0%83%e8%96%aa%7c14%e8%96%aa%7c%e5%81%a5%e8%ba%ab%e4%bf%b1%e4%b9%90%e9%83%a8%7c%e6%88%bf%e8%a1%a5%7c%e9%ab%98%e6%b8%a9%e8%a1%a5%e8%b4%b4%7c%e4%b8%8d%e5%8a%a0%e7%8f%ad%7c%e5%8c%85%e4%bd%8f%7c%e9%87%87%e6%9a%96%e8%a1%a5%e8%b4%b4%7c%e4%bd%8f%e6%88%bf%e8%a1%a5%e8%b4%b4%7c%e6%97%a0%e8%af%95%e7%94%a8%e6%9c%9f%7c%e5%85%8d%e6%81%af%e6%88%bf%e8%b4%b7; LastSearchHistory=%7b%22Id%22%3a%22d3c80d7a-4b6b-41d0-9ae7-b286cb664633%22%2c%22Name%22%3a%22python+%2b+%e5%8c%97%e4%ba%ac%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fjl%3d%25e5%258c%2597%25e4%25ba%25ac%26kw%3dpython%26sm%3d0%26sg%3d2d8d7bd1731e4c06a4fbbb6aa50d7eb6%26p%3d25%22%2c%22SaveTime%22%3a%22%5c%2fDate(1514356134523%2b0800)%5c%2f%22%7d",
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    }

response = requests.request("GET", url, headers=headers, params=querystring).content

# print(response)

soup = BeautifulSoup(response,'lxml')

# print(soup)
#html body div.main div.search_newlist_main div.newlist_main form div.clearfix div.newlist_wrap.fl div#newlist_list_div.newlist_list div#newlist_list_content_table.newlist_list_content
items = soup.select("div#newlist_list_content_table > table")
count = len(items) - 1
print(count)

job_count = re.findall(r"共<em>(.*?)</em>个职位满足条件",str(soup))[0]

pages = (int(job_count) // count) + 1

print(pages)