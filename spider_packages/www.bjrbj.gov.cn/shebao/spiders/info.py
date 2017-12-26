# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider
from shebao.libs.redis_lib import CRedis
from scrapy.http import FormRequest;
from scrapy.http import Request;
from scrapy.loader.processors import TakeFirst
from shebao.items import InfoItem
from shebao.items import OldPayItem
from shebao.items import MedPayItem
import json
import sys;
import os;
import time
import datetime

from six.moves.urllib.parse import urljoin, urlencode
from scrapy.utils.python import unicode_to_str
import urllib

#导入全局结构体
from shebao.bootstrap import Env
#scrapy crawl Info -a key=k2 -a username=*** -a password=1234555666 -a safecode=123344
class InfoSpider(Spider):
    name = "Info"
    #type:1
    #flag:3
    #j_username:340721198903232115
    #j_password:pz8316163
    #safecode:0036
    #x:43
    #y:15    
    login_url       = 'http://www.bjrbj.gov.cn/csibiz/indinfo/login.jsp';
    login_url2      = 'http://www.bjrbj.gov.cn/csibiz/indinfo/login.jsp?flag=3';#登录失败后重定向的登录结果页
    login_url3      = 'http://www.bjrbj.gov.cn/csibiz/indinfo/index.jsp';#登录成功后跳转到的个人中心首页信息页面
     
    
    
    login_check_url = 'http://www.bjrbj.gov.cn/csibiz/indinfo/login_check'
    info_url        = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indNewInfoSearchAction'#'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/ind_new_info_index.jsp';
    
    info_url2       = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!oldage'# 查询养老保险?searchYear=2015&time=1456368430861';#查询个人基本信息接口  从info_url跳转过来 即当前页面的refer=info_url
    info_url3       = 'http://www.bjrbj.gov.cn/csibiz/indinfo/search/ind/indPaySearchAction!medicalcare' #?searchYear=2015&time=1456368590937 医疗保险 当前时间的毫秒级别时间戳 time=new Date().getTime() = datetime.datetime.now().microsecond
    #info_params     = {} #info_url2 和 info_url3 需要两个参数 searchYear 和 time 
    
    def __init__(self, key = None, username = None, password = None, safecode = None):
        pass
        self.key      = str(key); #用来从redis中取出上一次  登录页面获取到的其他隐藏input 以及 headers cookie信息等
        self.username = str(username);
        self.password = str(password);
        self.safecode = str(safecode);
        
        self.obj_redis    = Env.get_redis_proxy();
        self.obj_take_first = TakeFirst();   
        self.cookies  = {}
    
    def start_requests(self):
        pass
        value    = self.obj_redis.get(self.key);
        #print "type:{0}, value:{1}".format(type(value), value);#str [(key,value),...]
        #获取cookie信息 发起登录检查
        if value is not None :
            formdata = {'j_username':self.username,'j_password':self.password,"safecode":self.safecode};
            dict_cookies = {};
            item = json.loads(value);#{k,v...}
            keys = item.keys();
            print "type:{0} keys:{1}".format(type(keys), keys);
            for k in keys:
                v=item[k]
                #print type(v);
                #print "k:{0}, v:{1}".format(k,v);
                if k == 'i_type':
                    formdata['type'] = str(v);
                    pass
                elif k == 'i_flag':
                    formdata['flag'] = str(v);
                    pass
                elif k == 'i_x':
                    formdata['x'] = str(v);
                    pass
                elif k == 'i_y':
                    formdata['y'] = str(v);
                    pass
                elif k == 'dict_cookies':
                    dict_cookies = v;
                    pass
                else:
                    pass #其他字段暂时不处理
             #i_status = item['i_status']; # must==0 php 层检查成功与否
     
            #注意formdata 里面的k v必须要求全部是 unicode 或者str否则会有错误
            #print "{0}:{1} formdata:{2} cookies:{3}".format(os.path.basename(__file__), sys._getframe().f_lineno, formdata, dict_cookies);
            Env.output(formdata=formdata, cookies=dict_cookies)
            self.cookies = dict_cookies;
                
            #需要一个数据类型判断 处理 因为username 不能为none 否则 unicode_to_str会粗错
            yield FormRequest(self.login_check_url, formdata=formdata,callback=self.parse_login_response, dont_filter=True,cookies=dict_cookies)
        else :
            yield Request(self.login_check_url, callback=self.parse_login_response, dont_filter=True) #如果过期则直接 会返回登录出差页面 10秒后自动跳转到登录页面
        
        
    #i_status -1 登录失败  -2 登录失败 cookie过期 需要重新获取信息登录
    def parse_login_response(self, response):
        
        # 
        #1 登录验证失败 会返回一个302 临时重定向结果 重定向http://www.bjrbj.gov.cn/csibiz/indinfo/login.jsp?flag=3 此时response.url=此页面
        #2 登录成功则直接跳转到一个页面 需要保存cookie信息 http://www.bjrbj.gov.cn/csibiz/indinfo/index.jsp
        pass
        url = response.url;
        item  = InfoItem()
        item['i_status'] = u'0'
        item['str_message'] = u'success'
        item['str_key'] = self.key
        item['kind']    = 'login' #在pipelines 的info 处理流程中需要 
        try:
            
            if url == self.login_url or self.login_url2 == url:
                #登录失败 提!= iRet:示信息 包含密码验证码 错误 以及 cookie过期等
                #print "{0}:{1} 登录失败,重定向到登录页面...{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, url);
                Env.output("登录失败,重定向到登录页面...{0}".format(url))
                #
                item['i_status'] =  u'-2';
                item['str_message'] =  u"login check fail, Redirct to login page !";
                
            elif self.login_url3 == url:
                #登录成功 单个回调函数中返回多个item和request
                #print "{0}:{1} 登录成功,跳转到信息页面...{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, url);
                Env.output("登录成功,跳转到信息页面...{0}".format(url))
                #print response;
                #rint response.body;
                #print response.url;
                pass
                #开启请求个人基本信息 info_url 后期优化同时添加查询 个人缴费信息请求
                yield Request(self.info_url, callback=self.parse_info_response, dont_filter=True, cookies = self.cookies)
                
                # 查询近三年 养老保险信息 info_url2
                # 查询近三年医疗保险信息  info_url3
                # searchYear=2015&time=1458551528524
                # 
                now_year = time.localtime()[0]
                for i in range(0,-3,-1):
                    year = now_year + i
                    now_time = datetime.datetime.now().microsecond
                    get_params = {'searchYear':year,'time':now_time}
                    info_url2 = "{0}?{1}".format(self.info_url2, urllib.urlencode(get_params))
                    Env.output(info_url2=info_url2)#old
                    yield Request(info_url2, callback=self.parse_info2_response, dont_filter=True, cookies = self.cookies)
                    info_url3 = "{0}?{1}".format(self.info_url3, urllib.urlencode(get_params))
                    Env.output(info_url3=info_url3)#med
                    yield Request(info_url3, callback=self.parse_info3_response, dont_filter=True, cookies = self.cookies)
                

            else:
                pass
                #unknow 
                #print "{0}:{1} 未知登录结果页!...{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, url);#有可能是login_url3
                Env.output("Unknow info page !{0}".format(url));
                raise Exception("Unknow info page!", url);
                
        except Exception as ex:
            item['i_status'] = -1;
            item['str_message'] = ex;
            #self.log("{0}:{1} Exception:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, sys.exc_info()), logging.ERROR);
            #print "{0}:{1} Exception:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, sys.exc_info());            
            Env.output(ex)
        finally:
            yield item
               
    def parse_info_response(self, response):
        #解析 获取个人基本信息接口
        url = response.url
        item = InfoItem()
        item['i_status'] = u'0'
        item['str_message'] = u'success'     
        item['str_key'] = self.key
        
        item['kind']        = u'base' #个人基本信息
        try:
            if url == self.info_url:
                pass
                #print "{0}:{1} 查询个人基本信息成功...{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, url)
                Env.output(u"查询个人基本信息成功...{0}".format(url));
                
                #解析表格
                #1 单位名称
                #单位名称、民族、参加工作日期、个人身份、户口性质、户口所在地、文化程度、申报月均工资收入
                tds = response.xpath('//td/text()').extract() #[] 
                Env.output(u" 个人基本信息 ：")

                #单位名称 第一个td 元素 
                str_tmp = tds[0];
                ltmp = str_tmp.split()
                item['unit_name'] = ltmp[1].strip() #单位名称
                
                #Env.output("ltmp:{0}".format(ltmp));#整体打印无法显示 中文形式unicode编码
                item['name']      = tds[9].strip() #姓名 strip 消除首尾空格
                item['nature']    = tds[18].strip() #名族
                item['begin_time']= tds[24].strip() #参加工作时间
                item['identity']  = tds[22].strip() #个人身份
                item['hkxinzhi']  = tds[27].strip()#户口性质
                item['hksuozaidi']= tds[29].strip() #户口所在地
                item['whdegree']  = tds[44].strip() #文化程度
                for k in item.keys():
                    Env.output(k=k, v=item[k])
                #月工资暂时忽略
                 
                    
                
            elif url == self.login_url or url == self.login_url2:
                pass
                #print "{0}:{1} 查询个人基本信息失败 ...{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, url)
                Env.output("查询个人基本信息失败...{0}".format(url))
                Env.get_logger().warning('查询个人基本信息失败...{0}'.format(url))
                item['i_status'] = u'-2'
                item['str_message'] = u'Redirect to login page...{0}'.format(url);
            
            else:
                #print "{0}:{1} 查询个人基本信息失败 未知结果 ...{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, url)             
                Env.output('查询个人基本信息失败 未知结果 {0}'.format(url))
                Env.warning('查询个人基本信息失败 未知结果 {0}'.format(url)) #记录到日志中
                item['i_status'] = -1;
                item['str_message'] = '查询个人基本信息失败 未知结果 {0}'.format(url)
                pass
            
        except Exception as ex:
            item['i_status'] = u'-1';
            item['str_message'] = ex;
            Env.output("Exception :{0}".format(ex))
            Env.get_logger().error(ex);
        finally:
            yield item;
            
    def parse_info2_response(self, response):
        #养老两个类目近3年的缴纳记录（缴费年月、缴费基数、单位缴纳、个人缴纳、缴纳单位名称）
        #
        pass
        url = response.url.split("?")[0]
        #Env.output(url)
        item = OldPayItem()
        item['i_status'] = u'0'
        item['str_message'] = u'success'
        item['str_key'] = self.key
        
        item['kind']        = u'old' #注意英文字符的unicode编码和 ascii编码一致
        item['data']        = []
        Env.output('养老保险...') #保证中文输出 正常
        try:
            if url == self.info_url2:
                #获取信息成功
                Env.output('开始解析养老保险...');
                se_tb = self.obj_take_first(response.xpath('//table'))
                se_tr = se_tb.xpath('.//tr');
    
                from shebao.items import PayItem
                
                #从第三个开始直到最后一个
                for idx,elem in enumerate(se_tr):
                    if idx < 2:
                        continue
                    tds = elem.xpath('.//td/text()').extract() #从当前路径提取所有
                    # 0 缴费年月 2 缴费基数 3 单位缴费 4 个人缴费 5 缴费单位名称
                    Env.output("{0} {1} {2} {3} {4}".format(tds[0].strip(), tds[2].strip(), tds[3].strip(), tds[4].strip(), tds[5].strip()))
                    #print tds
                    pay_item = PayItem()
                    pay_item['jfny'] = tds[0].strip() #首尾空白字符的消除
                    pay_item['jfjs'] = tds[2].strip()
                    pay_item['dwjf'] = tds[3].strip()
                    pay_item['grjf'] = tds[4].strip()
                    pay_item['jfdw'] = tds[5].strip()
                    item['data'].append(pay_item)
                
            elif url == self.login_url or url == self.login_url2:
                #登录
                item['i_status'] = u'-2'
                item['str_message'] = u'Redirect to login page...{0}'.format(url);
            else:
                Env.output("查询个人养老 未知接口返回!{0}".format(url))
                Env.get_logger().error("查询个人养老 未知接口返回!{0}".format(url))
                item['i_status'] = -1;
                item['str_message'] = "查询个人养老 未知接口返回!{0}".format(url)                
         
        except Exception as ex:
            Env.output("Exception:{0}".format(ex))
            Env.get_logger().error(ex)
        finally:
            yield item
    
    def parse_info3_response(self, response):
        pass
        #医疗 （缴费年月、缴费基数、单位缴纳、个人缴纳、缴纳单位名称）
        url = response.url.split("?")[0]
        #Env.output(url)
        #Env.output(self.info_url3)
        item = MedPayItem()
        item['i_status'] = u'0'
        item['str_message'] = u'success'   
        item['str_key']    = self.key
        item['kind']        = u'med'
        item['data']        = []
        Env.output(u'医疗保险...') # 加不加 u 都可以正常输出 json.dumps 的时候 加了特殊选项
        #Env.output(response.body)
        
            
        try:
            if url == self.info_url3:
                #查询医疗保险缴费情况成功
                #获取信息成功
                
                Env.output("开始解析医疗保险...")
                se_tb = self.obj_take_first(response.xpath('//table'))
                se_tr = se_tb.xpath('.//tr');
    
                from shebao.items import PayItem
                
                #从第三个开始直到最后一个
                for idx,elem in enumerate(se_tr):
                    if idx < 2:
                        continue
                    tds = elem.xpath('.//td/text()').extract() #从当前路径提取所有
                    # 0 缴费年月 2 缴费基数 3 单位缴费 4 个人缴费 5 缴费单位名称
                    Env.output("{0} {1} {2} {3} {4}".format(tds[0].strip(), tds[2].strip(), tds[3].strip(), tds[4].strip(), tds[5].strip()))
                    pay_item = PayItem()
                    pay_item['jfny'] = tds[0].strip()
                    pay_item['jfjs'] = tds[2].strip()
                    pay_item['dwjf'] = tds[3].strip()
                    pay_item['grjf'] = tds[4].strip()
                    pay_item['jfdw'] = tds[5].strip()     
                    item['data'].append(pay_item)
            elif url == self.login_url or url == self.login_url2:
                #
                item['i_status'] = u'-2'
                item['str_message'] = u'Redirect to login page...{0}'.format(url);                
            else:
                #社保网站升级导致
                Env.output("查询个人医疗保险 未知返回!{0}".format(url))
                Env.get_logger().error("查询个人医疗保险 未知返回!{0}".format(url))
                item['i_status'] = u'-1';
                item['str_message'] = "查询个人医疗保险 未知返回!{0}".format(url)                 
            
        except Exception as ex:
            Env.output("Exception:{0}".format(ex))
            Env.get_logger().error(ex)   
        finally:
            yield item
        
    