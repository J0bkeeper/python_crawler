#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.22 12:33'

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text,'html.parser')
soup.find(name='h3',attr={'class':'t'})
soup.find_all(name='h3')

