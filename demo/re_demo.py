#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.22 13:01'

import re

text = "百度一下，你就知道123432"
reg = ".*?\d"
result = re.match(reg,text).group()

print(result)