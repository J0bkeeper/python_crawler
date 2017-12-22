#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
爬虫爬取纯妹妹网每个页面的图片
http://bbs.fishc.com/thread-64577-1-1.html
"""
import urllib.request
import urllib.error
from http import server, client #方便后面能够捕获到此类相关的异常
import os, re

#伪装成浏览器
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

def urlOpen(url):
    global header
    req = urllib.request.Request(url, None, header)
    return urllib.request.urlopen(req).read()

def tryToGet(url):
    errorTimes = 0 #记录出错次数，超过5次则放弃访问该页面
    while errorTimes != 5:
        try: #尝试访问该页面
            errorTimes += 1
            return urlOpen(url)
        except: #若出现异常则忽略，重新访问
            pass

    return None #超过5次访问失败，返回空值

#获取子页面
def getSubpage(url):
    response = tryToGet(url)
    if response != None:
        html = response.decode('utf-8')
        #用于获取标题栏中子页面url的正则表达式
        p = re.compile(r'<a href="/(.*\.html)" class="tag-font-size-14">')
        return p.findall(html)
    else:
        print('**********当前页面获取失败')
        return list()

imgCount = 1#图片计数器
def saveImgInPage(url):
    global imgCount
    print('**********正在获取页面' + url)
    response = tryToGet(url)
    if response != None:
        html = response.decode('utf-8')
        #获取图片url的正则表达式
        p = re.compile(r'<img .* src="(.*\.jpg)"')
        imgList = p.findall(html)

        for each in imgList:
            response = tryToGet(each)
            if response != None:
                #保存图片
                with open(str(imgCount) + '.jpg', 'wb') as f:
                    f.write(response)
                print('**********目前已成功获取%d张图片!' % imgCount)
                imgCount += 1

    else:
        print('**********当前页面获取失败!')

def work():
    if not os.path.isdir('妹子图'):
        os.mkdir('妹子图')
    os.chdir('妹子图')
    
    url = 'http://www.chunmm.com/'
    subpageList = getSubpage(url)#获取子页面
    subpageList.insert(0, '')#加入首页

    for each in subpageList:#爬取每个页面上的图片
        saveImgInPage(url + each)
    

if __name__ == '__main__':
    work()