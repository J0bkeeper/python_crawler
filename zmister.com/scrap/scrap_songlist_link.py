# coding:utf-8
'''
    @author:zmister.com
    微信公众号：州的先生
    @time:2016/12/27
'''
import requests
import re
import pymongo
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from selenium import webdriver

# 设置MongoDB数据库连接
# 设置MongoDB连接信息
client = pymongo.MongoClient('localhost',27017)
baidu_music = client['baidu_music']
song_list = baidu_music['song_list']

# 获取歌单
def get_song_list(page):
    songListUrl = 'http://music.baidu.com/songlist/tag/%E5%85%A8%E9%83%A8?orderType=1&offset={0}'.format(page)
    print(songListUrl)
    wbdata = requests.get(songListUrl).content
    soup = BeautifulSoup(wbdata,'lxml')
    songListLink = soup.select("p.text-title > a ")
    for s in songListLink:
        title = s.get('title')
        link = s.get('href')
        data = {
            "title":title,
            "link":link
        }
        song_list.insert_one(data)
        print("数据写入成功")

if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map_async(get_song_list,range(0,7880,20))
    pool.close()
    pool.join()

