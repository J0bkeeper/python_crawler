# -*- coding: utf-8 -*-
import sys
#为了使得 from shebao.libs.mysql_lib 这样 在任意目录运行文件都能使用 应该将应用程序目录添加到搜索目录中

import scrapy
#from scrapy.contrib.loader.processor import TakeFirst
from scrapy.loader.processors import TakeFirst
from shebao.items import LoginItem # import special class or function
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.spiders import Spider

import json #import module and package 
import logging
import os;
import pickle

from shebao.bootstrap import Env
class LoginSpider(Spider):
    name = "Login"
    category = None
    login_url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/login.jsp'
    prefix_safecode_url = 'http://www.bjrbj.gov.cn'
    #validate_img = 'http://www.bjrbj.gov.cn/csibiz/indinfo/validationCodeServlet.do' #d=
    #login headers
    #Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    #Accept-Encoding:gzip, deflate, sdch
    #Accept-Language:zh-CN,zh;q=0.8
    #Connection:keep-alive
    #Cookie:JSESSIONID=0425CFF7A8ECA7E1016B3B0BF3EBDE6B; JSESSIONID=MMpWWDTT1DdYMps1g5RKtwtg9BlKJ2dcw0KHZvVf8PGhhnJt1Mfq!651493767; _trs_ua_s_1=5zte_365_ikq7ya4q; _gscu_2145764248=53970539htcyqo96; _gscbrs_2145764248=1; sto-id-jzxx=GGBEKIMA; qx2nR3OHg7=MDAwM2IyYWYyZjQwMDAwMDAwMjEwJ05vNjUxNDU1NzA1NDcz; AXM6mOFhT5=MDAwM2IyYWYyZjQwMDAwMDAwMjYwcgRyPhYxNDU1NzA1NDc4; _trs_uv=7ov4_365_ijy0iorn; mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwSkY+NmkxNDU1Nzk0NDMy; _gscu_2065735475=53970539uygds896; _gscs_2065735475=t55760686ds2hb417|pv:21; _gscbrs_2065735475=1
    #Host:www.bjrbj.gov.cn
    #Upgrade-Insecure-Requests:1
    #User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36
    def __init__(self, key = None):
        pass
        self.key      = key;
        self.obj_take_first  = TakeFirst();
               
    def start_requests(self):
        pass
        # set headers
        yield Request(self.login_url, callback=self.parse_login_response, dont_filter=True) #http://www.bjrbj.gov.cn/csibiz/indinfo/login.jsp
        
    #在回调函数中，你可以解析网页响应并返回项目对象和请求对象或两者的迭代
    def parse_login_response(self, response):
        items = [];
        item = LoginItem(); 
        try :
            #...
            #...save headers to redis and save input to item and then to redis (key=cateGory value=response)
            # save input field type flag j_password
            # save twok cookie to redis 只需要如下两个cookie即可登录
            #Set-Cookie:mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwZmYWU2kxNDU1ODk2MDAx;path=/
            #Set-Cookie:JSESSIONID=65C4F4C83F135DE529788EEDDBE18237; Path=/csibiz/indinfo   
            
            #解析cookie存储
            headers = response.headers.items(); #[(key,value),...]
            cookies = {};
            for header in headers:
                k = header[0];
                if k == 'Set-Cookie' :
                    lv = header[1];#mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwZmYWU2kxNDU1ODk2MDAx;path=/ ... list
                    for cookie in lv:
                        pass
                        lcv = cookie.split(';');#mjrzMBJgZO=MDAwM2IyYWYyZjQwMDAwMDAwMDgwZmYWU2kxNDU1ODk2MDAx
                        lckv= lcv[0].split("=");#
                        cookies[lckv[0]] = str(lckv[1]);
                    
            item['dict_cookies'] = cookies;
            
            safecode_path = self.obj_take_first(response.xpath('//form[@id="indform"]//img[@id="indsafecode"]/@src').extract());
            #特殊的对象 可以像字典一样访问
            
            #item.str_key = '1';
            #
            item['str_key']    = self.key
            #print "dir(response):{0}".format(dir(response))
            
            #item['obj_response']   = pickle.dumps(response);
            # python __call__ 模拟仿函数调用
            item['i_type'] = self.obj_take_first(response.xpath('//form[@id="indform"]//input[@name="type"]/@value').extract());#1
           
            item['i_flag'] = self.obj_take_first(response.xpath('//form[@id="indform"]//input[@name="flag"]/@value').extract());#3
            item['str_username'] = self.obj_take_first(response.xpath('//form[@id="indform"]//input[@name="j_username"]/@value').extract());
            item['str_password'] = self.obj_take_first(response.xpath('//form[@id="indform"]//input[@name="j_password"]/@value').extract());
            item['str_safecode'] = self.prefix_safecode_url+safecode_path;
            item['i_x'] = u'23';#暂时随便写 未找到来源
            item['i_y'] = u'20';#暂时随便写
                     
            #object.__getstate__()/__dict__ object.__setstate__(state) 序列化和反 序列化调用的函数 https://docs.python.org/3.4/library/pickle.html#object.__getstate__
            item['i_status'] = u'0';
            item['str_message'] = 'success';
            #print "{0}:{1} item:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, item); #程序会自己打印debug 日志记录item结果
            #msg = "{0}:{1} item:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, pickle.dumps(item));
            #self.log(msg, logging.INFO);              
            print "------------------------登录请求返回值----------------------";
            #print "{0}:{1} item:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, item.items());
            print item
            print type(item)
            print item.items()
            print "------------------------登录请求返回值----------------------";
            
        except Exception as ex:
            #print sys._getframe().f_lineno
            item['i_status'] = str(-1);
            item['str_message'] = ex;
            Env.get_logger().error(ex)
        finally:
            items.append(item);
            return items;
        
                
    
if __name__ == "__main__":
    
        
    from shebao.opts.opt import Env
    
    print Env.get_logger()._get_format() #('./shebao/spiders/login.py', 116)