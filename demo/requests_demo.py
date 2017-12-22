#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.22 12:29'

import requests

response = requests.get("http://www.baidu.com")

print(response.text)