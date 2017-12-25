#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.25 16:27'

from selenium import webdriver


url = "http://www.mouser.cn/productdetail/vishay-semiconductors/egp51g-e3-c?qs=sGAEpiMZZMtbRapU8LlZD1zUshIXr8GERRWYotATcRLLDvP133TF7w%3D%3D"


browser = webdriver.Chrome()
browser.get(url)
print(browser.page_source)
# elem = browser.find_element_by_id("spnMouserPartNumFormattedForProdInfo")

# import requests
# import re
# from lxml import html as etree
#
#
# headers = {
#     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
# html1 = requests.get(url, headers=headers)
# data = html1.text
# print(data)
# pattern = re.compile('spnMouserPartNumFormattedForProdInfo',re.S)
# urls = re.findall(pattern, data)
# print(urls)