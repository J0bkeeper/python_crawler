#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 16:07'

import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
import time

CONFIGFILE = "password.conf"
config = configparser.RawConfigParser()
config.read(CONFIGFILE)
user = config.get("qq1","user")
passwd = config.get("qq1","passwd")
qq = config.get("qq1","qq")


driver = webdriver.Chrome()
driver.maximize_window()

def get_shuoshuo(qq):
    driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(5)
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a == True:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()  # 选择用户名框
        driver.find_element_by_id('u').send_keys(user)
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(passwd)
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        content = driver.find_elements_by_css_selector('.content')
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for con, sti in zip(content, stime):
            data = {
                '时间': sti.text,
                '说说': con.text
            }
            print(data)
        pages = driver.page_source
        soup = BeautifulSoup(pages, 'lxml')

    cookie = driver.get_cookies()
    cookie_dict = []
    for c in cookie:
        ck = "{0}={1};".format(c['name'], c['value'])
        cookie_dict.append(ck)
    i = ''
    for c in cookie_dict:
        i += c
    print('Cookies:', i)
    print("==========完成================")

    driver.close()
    driver.quit()


if __name__ == "__main__":
    get_shuoshuo(qq)