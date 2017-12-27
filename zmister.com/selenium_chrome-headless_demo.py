#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 16:47'


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()
driver.get("https://www.baidu.com")
driver.save_screenshot("baidu{}.png".format(datetime.datetime.now()))
time.sleep(20)
driver.close()
driver.quit()