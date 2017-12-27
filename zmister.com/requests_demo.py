#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.27 10:24'

import requests

url = "http://zmister.com"
data = requests.get(url)
print(data.status_code)
print("-"*20)
print(data.content)
print(data.content.decode())
