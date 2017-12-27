#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 16:47'


from selenium import webdriver
import time
import datetime


# driver = webdriver.Chrome()
# driver = webdriver.Firefox()
# driver = webdriver.FirefoxOptions()
# driver = webdriver.FirefoxProfile()
driver = webdriver.PhantomJS()
driver.maximize_window()

driver.get('https://www.baidu.com')
driver.save_screenshot('baidu-{}.png'.format(datetime.datetime.now()))
# driver.execute_script("JS代码")
time.sleep(20)
driver.close()
driver.quit()