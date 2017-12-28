#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.28 11:14'


import requests
from bs4 import BeautifulSoup
import nltk


#1.爬取ChinaDaily全站网页URL
def get_all_link(url):
    try:
        # 分割网址
        host = url.split('/')
        # print(host[2])
        response = requests.get(url).text
        soup = BeautifulSoup(response,'lxml')
        for link in soup.find_all('a'):
            # 判断网页中提取的URl形式
            if link.get('href') not in pages and link.get('href') is not None:
                if link.get('href').startswith('http'):
                    if link.get('href').split('/')[2] == host[2]:
                        newpage = link.get('href')
                        # print(newpage)
                        pages.add(newpage)
                        get_all_link(newpage)
                elif link.get('href').startswith('/'):
                    newpage = link.get('href')
                    pages.add(newpage)
                    newpage_url = 'http://'+host[2]+newpage
                    # print(newpage_url)
                    get_all_link(newpage_url)
        print('url数量：'+str(len(pages)))
    except BaseException as e:
        print('程序出错：{0}'.format(e))


#2.请求爬取的URL并解析网页单词
#解析网页单词并写入文本文件
def resolve_html(url):
    response = requests.get(url).content
    soup = BeautifulSoup(response,'lxml')
    # 替换换行字符
    text = str(soup).replace('\n','').replace('\r','')
    # 替换<script>标签
    text = re.sub(r'\<script.*?\>.*?\</script\>',' ',text)
    # 替换HTML标签
    text = re.sub(r'\<.*?\>'," ",text)
    text = re.sub(r'[^a-zA-Z]',' ',text)
    # 转换为小写
    text = text.lower()
    text = text.split()
    text = [i for i in text if len(i) > 1 and i != 'chinadaily']
    text = ' '.join(text)
    print(text)
    with open("words.txt",'a+',encoding='utf-8') as file:
      file.write(text+' ')
      print("写入成功")


#3.对单词文本文件进行词频处理
#对单词文本文件进行词频处理
def resolve_words():
    corpath = 'words'
    wordlist = PlaintextCorpusReader(corpath,'.*')
    allwords = nltk.Text(wordlist.words('words.txt'))
    print("单词总数",len(allwords))
    print("单词个数",len(set(allwords)))
    stop = stopwords.words('english')
    swords = [i for i in allwords if  i not in stop]
    print("去除停用词的单词总数：",len(swords))
    print("去除停用词的单词个数：",len(set(swords)))
    print("开始词频统计")
    fdist = nltk.FreqDist(swords)
    print(fdist.most_common(3000))
    for item in fdist.most_common(3000):
        print(item,item[0])
        with open('words3000.txt','a+',encoding='utf-8') as file:
            file.write(item[0]+'\r')
    print("写入完成")


if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map_async(resolve_html,urllist)
    pool.close()
    pool.join()
    print('运行完成')