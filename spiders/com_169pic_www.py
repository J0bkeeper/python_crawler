#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
python爬虫某著名美女美腿网站
http://bbs.fishc.com/thread-74707-1-1.html
"""
import re
import urllib.request as ur
import time
import os
import threading
from urllib.error import URLError, HTTPError

base_path = os.path.dirname(os.path.abspath(__file__))
folerpath = base_path

def gethtml(url):
    try:
        req  = ur.Request(url)
    except ValueError as e:
        print('value Error',e.reason)
        return
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
    
    try:
        response = ur.urlopen(req)
    except URLError as e:
        print('URLError reason:',e.reason)
        return
    try:
        html = response.read()
    except:
        return
    return html

'''保图片存到本地'''
def writeImgToFolder(hexData,subfolerpath):
    with open(subfolerpath,'wb') as fp:
        print(subfolerpath)
        fp.write(hexData)

'''
将当前图片写真页面中的图片，保存到本地
http://www.169bb.com/gaogensiwa/2016/0808/36632.html
文件夹名称即为图片标题名
'''
def getImgSrcAndDownload(html,needchangeFolder,lastfolder,lastnum):
    global folerpath
    start = html.find('<title>')
    end = html.find('</title>',start)

    '''如果需要修改图片文件夹名称，则修改'''
    '''否则用之前的名称'''
    if (needchangeFolder):
        imgtitle = html[start+len(r'<title>'):end]
        # subfolerpath  = folerpath +"\\"+imgtitle
        subfolerpath  = folerpath + imgtitle
        # print(subfolerpath)
        num = 0
    else:
        num = lastnum
        subfolerpath = lastfolder
    try:
        os.mkdir(subfolerpath)
    except:
        pass
    pat = re.compile(r'"center"><img src="')
    iter1 = pat.finditer(html) 
    for i in iter1:
        #print(i.group(),i.span())
        tmp  = i.group()
        tail = html.find(' ',i.span()[1])
        #print(html[i.span()[1]:tail-1])
        theImgSrc = html[i.span()[1]:tail-1]
        '''此处得到图片的字节集 '''
        imghex = gethtml(theImgSrc)
        # imgPath = subfolerpath +"\\" + str(num) + '.jpg'
        imgPath = subfolerpath + "/" + subfolerpath[len(folerpath):] + str(num) + '.jpg'
        # print(imgPath)
        writeImgToFolder(imghex,imgPath)
        num += 1

    '''代表没找到图片,特征码不一样，改成查找center'''
    if (num == lastnum):
        pat = re.compile(r'"center"')
        iter1 = pat.finditer(html) 
        for i in iter1:
            tmp  = i.group()
            tail = html.find('jpg',i.span()[1])
            theImgSrc = html[i.span()[1] + 3 + len('<img src=') + 2:tail+3]
            print(theImgSrc)
            '''此处得到图片的字节集'''
            imghex = gethtml(theImgSrc)
            # imgPath = subfolerpath +"\\" + str(num) + '.jpg'
            imgPath = subfolerpath + "/" + imgtitle + str(num) + '.jpg'
            writeImgToFolder(imghex,imgPath)
            num += 1       

    return (subfolerpath,num)
'''
得到第一层每一页中图片页面的地址
比如http://www.169bb.com/gaogensiwa/2016/0808/36632.html
http://www.169bb.com/gaogensiwa/2016/0808/36632_2.html
'''

def _getAllPageUrl(url):
    subhtml = gethtml(url)
    if (subhtml == None):
        return
    subhtml = subhtml.decode('GBK')
    tup = getImgSrcAndDownload(subhtml,True,'',0)
    lastFolder = tup[0]
    lastnum  = tup[1]
    for j in range(2,6):
        nextpage = url
        nextpage  = nextpage[0:len(nextpage)-5] + '_' +str(j)+'.html'
        #print('nextpage:',nextpage)
        subhtml = gethtml(nextpage)
        if (subhtml == None):
            continue
        subhtml = subhtml.decode('GBK')
        tup = getImgSrcAndDownload(subhtml,False,lastFolder,lastnum)
        lastFolder = tup[0]
        lastnum  = tup[1]
        time.sleep(0.1) 

def getAllPageUrl(html):
    pat = re.compile(r'http://www.169pic.com/gaogensiwa/\d{4}/\d{4}/\d{5}.html')
    iter1 = pat.finditer(html)
    thread_arr=[]
    for i in iter1:
        t = threading.Thread(target=_getAllPageUrl,args = (i.group(),))
        thread_arr.append(t)

    for i in thread_arr:
        i.start()
    for i in thread_arr:
        i.join()

def main():
    global folerpath
    folerpath = os.getcwd()
    folerpath += r'/169mm/'
    try:
        os.mkdir(folerpath)
    except:
        pass
    os.chdir(folerpath)
    '''第一层需要遍历的页数'''
    for i in range(1,3):
        html  = gethtml('http://www.169pic.com/gaogensiwa/list_3_%d.html'%i)
        if (html == None):
           continue
        html = html.decode('GBK')
        getAllPageUrl(html)

if __name__=='__main__':
    main()
