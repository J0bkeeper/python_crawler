#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.22 12:29'

import re

url1 = "http://www.ashghal.gov.qa/en/Tenders/TenderBriefDocuments/(06)%20-%20C%20-%20Employer's%20Requirements%20STC%20092%20R.pdf"

url2 = "http://www.ashghal.gov.qa/en/Tenders/TenderBriefDocuments/STC-118-2017%20-%20C%20-%20Employer's%20Requirement.pdf"

result = "acc".replace("a","b")
print(result)

res1 = url1.replace("(","%28").replace(")","%29").replace("'","％27")
res2 = url2.replace("(","%28").replace(")","%29").replace("'","％27")
print(res1)
print(res2)