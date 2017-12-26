# -*- coding: utf-8 -*-
#获取社保的验证码 要求使用同一个cookie 获取
from scrapy.spiders import Spider
from scrapy.loader.processors import TakeFirst

import scrapy
import json
import sys
import os.path;

from shebao.libs.redis_lib import CRedis
from shebao.items import VerifyCodeItem


from scrapy.http import FormRequest;
from scrapy.http import Request;

#此爬虫 只用来后台验证 实际使用中 只提供cookie和url给前端 由前端自己获取图片
from shebao.bootstrap import Env
#scrapy crawl VerifyCode -a key=k3
class VerifyCodeSpider(Spider):
    
    name         = "VerifyCode";
    safecode_url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/validationCodeServlet.do';
    
    def __init__(self, key=None):
        pass
        self.obj_redis = Env.get_redis_proxy();
        self.key       = key;
        self.obj_take_first = TakeFirst()
        self.request_cookies = {}
        
       
        
    def start_requests(self):
        pass
        value = self.obj_redis.get(self.key);
        #dict_cookies = {}; #空cookies 请求的验证码 不能验证通过
        if  value is not None:
            pass #要求未过期
            item  = json.loads(value);# dict 
            self.request_cookies = item['dict_cookies'];#str
        #dont_filter 表示不应该忽略重复的请求
        yield Request(self.safecode_url, callback=self.parse_safecode_response, dont_filter=True,cookies=self.request_cookies);
        
        
    def parse_safecode_response(self, response):
        #解析img 验证码 并识别结果
        #<body><img style="-webkit-user-select: none" src="http://www.bjrbj.gov.cn/csibiz/indinfo/validationCodeServlet.do"></body>
        #注意 response.body 就是一个图片的二进制流 存储为jpg文件 能直接查看到验证码图片
        pass
        item  = VerifyCodeItem();
        try:
            #如果cookie 过期 返回来的cookie和 请求的会不一致 则也要求重新获取登录

            item['i_status']    = u'0';
            item['str_message'] = u'success';
            item['str_key']     = self.key;
            item['request_cookies'] = self.request_cookies
            baseurl = Env.get_config().get('application', 'baseurl')
            item['file_path']   = baseurl + "www.bjrbj.gov.cn/data/"+self.key+"_safecode.jpg"; #后期优化做文件写入返回值判断 要求在 www.bjrbj.gov.cn/shebao目录运行 后期优化
           
            #需要解析cookie 和之前请求的是否一致
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
                               
            
            item['response_cookies'] = cookies;  
            print "--------------请求验证码返回值-----------------";
            #print response.headers
            #print "{0}:{1} items:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, item.items());
            #Env.output(cookies=cookies) #请求验证码返回的cookies 值 如果与请求时的cookies不一致 则表面上一个cookies已经过期 则当前的验证码 在接下来的 信息获取登录中是无效 会直接跳转到登录页面
            Env.output(item.items())
            print "--------------请求验证码返回值-----------------"
            fp = open(item['file_path'], 'w')
            fp.write(response.body);
            #imge = Image.open(item['file_path']); 验证码识别技术 后期优化
            #item['safecode'] = image_to_string(image) # item['safecode'] = image_file_to_string(item['file_path'])
            #item['img_src'] = src;
        except:
            item['i_status'] = u'-1';
            item['str_message'] = sys.exc_info();
            Env.output(sys.exc_info())
            Env.get_logger().error(sys.exc_info())
        finally:
            yield item
        
if __name__ == "__main__":
    print __file__;
    file = sys.argv[1];
    im = Image.open(file)
    print image_to_string(im)