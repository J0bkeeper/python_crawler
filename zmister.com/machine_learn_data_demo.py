#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.28 08:48'


import numpy as np
import pandas as pd
import pymongo
import matplotlib.pyplot as plt

# 链接MongoDB
conn = pymongo.MongoClient(host='localhost', port=27017)
toutiaohao = conn['toutiaohao']
news = toutiaohao['news']

data = pd.DataFrame(list(news.find()))
del data['_id']

#去除重复值
data = data.drop_duplicates(subset='title')

#按照阅读量排序，看看前10都是些什么文章：
data = data.sort_values('readcount',ascending=False)
data.head(10)

#再看看各个类别的占比
data['category'].value_counts().reset_index()


#画图 分类占比饼图
plt.style.use('ggplot')
plt.figure(figsize=(6,6))
plt.pie(data['category'].value_counts().reset_index()['category'],
        labels=data['category'].value_counts().reset_index()['index'])


#画图 分类数量柱状图
plt.figure(figsize=(15,10))
plt.bar(np.arange(len(data['category'].value_counts().reset_index())),data['category'].value_counts().reset_index()['category'])
plt.xticks(np.arange(len(data['category'].value_counts().reset_index())),data['category'].value_counts().reset_index()['index'],rotation=50)


#最后看看各个头条号的阅读量
data_groupby_author_to_readcount = data.groupby('author')['readcount'].sum().reset_index().sort_values('readcount',ascending=False)
data_groupby_author_to_readcount.head(10)

#前10的阅读量合计
data_groupby_author_to_readcount.head(10)['readcount'].sum()

#所有头条号的阅读量合计为
data_groupby_author_to_readcount['readcount'].sum()

#画图 头条号类型比率饼图
data.drop_duplicates(subset='author').groupby('category')['author'].count().reset_index()
