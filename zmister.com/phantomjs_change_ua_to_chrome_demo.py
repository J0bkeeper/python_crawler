#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.28 08:08'


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def editUserAgent():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])
    driver.get("http://service.spiritsoft.cn/ua.html")
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    user_agent = soup.find_all('td', attrs={
        'style': 'height:40px;text-align:center;font-size:16px;font-weight:bolder;color:red;'})
    for u in user_agent:
        print(u.get_text().replace('\n', '').replace('', ''))
    driver.close()


def defaultPhantomJS():
    driver = webdriver.PhantomJS()
    driver.get("http://service.spiritsoft.cn/ua.html")
    source = driver.page_source
    soup = BeautifulSoup(source,'lxml')
    user_agent = soup.find_all('td',attrs={'style':'height:40px;text-align:center;font-size:16px;font-weight:bolder;color:red;'})
    for u in user_agent:
        print(u.get_text().replace('\n','').replace('',''))
    driver.close()


if __name__ == "__main__":
    # defaultPhantomJS()
    editUserAgent()