# coding:utf-8
'''
    @author:zmister.com
    微信公众号：州的先生
    @time:2016/12/27
'''
import requests
import re
import pymongo
import json
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from selenium import webdriver
import random

# 设置MongoDB数据库连接
# 设置MongoDB连接信息
client = pymongo.MongoClient('localhost',27017)
baidu_music = client['baidu_music']
song_list = baidu_music['song_list']
songlist_info = baidu_music['songlist_info']
error_link = baidu_music['error_link']

# 代理列表
prolist = ["180.139.159.33:80","120.52.72.59:80","113.18.193.5:80","113.18.193.24:80"]

songlistlink = []
for s in song_list.find({},{"link":1,"_id":0}):
    songlistlink.append(s['link'])

# 获取歌单详细信息
def get_songlist_info(songlisturl):
    proxies = {
        "http": "http://{0}".format(random.choice(prolist)),
    }
    try:
        url = "http://music.baidu.com"+songlisturl
        print(url)
        wbdata = requests.get(url).content
        soup = BeautifulSoup(wbdata,'lxml')
        # 歌单名字
        list_name = soup.h1.get_text()
        # 创建者
        list_user = soup.find(name="a",class_="songlist-info-username").get_text()
        # 歌单标签
        list_tags = soup.select("div.songlist-info-tag > a")[0].get_text()
        # 播放次数
        list_count = soup.find(name="span",class_="songlist-listen").get_text()
        # 收藏次数
        list_collect = soup.find(name="em",class_="collectNum").get_text()
        # 歌单歌曲
        list_music = soup.select("div.normal-song-list.song-list.song-list-hook.clear.song-list-btnBoth.song-list-btnTop.song-list-btnBottom > ul > li")
        for m in list_music:
            sdata = json.loads(m['data-songitem'])
            sname = sdata['songItem']['sname']
            sauthor = sdata['songItem']['author']

            data = {
                "list_name":list_name,
                "list_user":list_user,
                "list_count":list_count,
                "list_collect":list_collect,
                "list_tage":list_tags,
                "sname":sname,
                "sauthor":sauthor,
            }
            songlist_info.insert_one(data)
            print(data)
    except BaseException as e:
        # error_link.insert_one(songlisturl)
        print("程序运行出错：%s" % e)
        # error_link.insert_one(songlisturl)

if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map_async(get_songlist_info,songlistlink)
    pool.close()
    pool.join()
    # get_songlist_info("/songlist/6444")
    # print(songlistlink)
