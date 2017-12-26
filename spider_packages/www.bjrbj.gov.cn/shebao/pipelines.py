# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.loader.processors import TakeFirst
from shebao.items import LoginItem
import json
import pickle
import sys
import os

import ConfigParser
from shebao.bootstrap import Env
#reload(sys) 已经使用更好的方式 在文件头部添加utf-8解决
#sys.setdefaultencoding('utf-8')

class ShebaoPipeline(object):
    def __init__(self):
        self.obj_redis = Env.get_redis_proxy();
        self.obj_take_first = TakeFirst();
    def process_item(self, item, spider):
        #print "{0}:{1} spider.name:{2} items:{3}".format(os.path.basename(__file__), sys._getframe().f_lineno, spider.name, item.items())
        
        #Env.output(spider.name, item.items()) #这句话 需要判断 item.items() 是不是dict [] 或者 () 或者 一般类型
        Env.get_logger().info(spider_name=spider.name, items=item.items())
        try :
            if spider.name == 'Login':          
                pass
                #type(item) LoginItem
                key  = item['str_key'];

                #value = json.dumps(item.items()); #不能直接json.dumps(item) json.dumps只支持列表序列化
                #value = pickle.dumps(data); #只要标准对象实现object.__getstate__()/__dict__ object.__setstate__(state) 序列化和反 序列化调 才可以序列化
                #pickle 序列化不方便查看 采用json.dumps(dict)格式
                keys = item.keys();
                data = {};
                
                for k in keys:
                    data[k] = item[k];
                    #print type(item[k]); unicode类型
                Env.output("data:{0}".format(data))
                value = json.dumps(data);
               
                time = 5*60*100000; #测试时间弄长些
                #print 'key:{0} value:{1}'.format(key, value);
                #print type(value);
                #Env.output(key=key,time=time,value=value)
                self.obj_redis.setex(key, time, value)
 
            elif spider.name == 'Info':
                pass
                #做编码格式转换 存储
                
                kind = item['kind'] #base med old 基本 信息 医疗保险 养老保险
                #print type(kind)
                #Env.output(kind=kind, type=type(kind))
                str_key = item['str_key'] #通常和用户userId+时间组合 唯一标示用户某次查询请求
                
                if kind == 'base':
                    pass
                    str_key = "{0}_base".format(str_key) #防止和 Login冲突
                    for k in item.keys():
                        v = json.dumps(item[k], ensure_ascii=False)
                        self.obj_redis.hset(str_key, k, v)
                elif kind == 'med':#医疗保险
                    pass
                                     
                    str_key = "{0}_med".format(str_key) #防止和 Login冲突                 
                    #后期优化 item['i_status'] != 0的判断处理
                    data = item['data']
                   
                    for ldata in data:#Pay_Item
                        pass
                        ldata = self.item_to_dict(ldata)
                        ldata = json.dumps(ldata, ensure_ascii=False) #Pay_Item
                        self.obj_redis.lpush(str_key, ldata)
                    
                        
                elif kind == 'old':#养老保险
                    pass
                    str_key = "{0}_old".format(str_key) #防止和 Login冲突
                    data    = item['data']
                    for ldata in data:
                        pass
                        ldata = self.item_to_dict(ldata)
                        ldata = json.dumps(ldata, ensure_ascii=False) #Pay_Item
                        self.obj_redis.lpush(str_key, ldata)
                        
                elif kind == 'login':#登录
                    pass
                else:
                    pass
                    Env.output("Not define kind...!", kind)
                    Env.get_logger().warning("Not define kind...!", kind) #暂时未定义的处理流程
                
            elif spider.name == 'VerifyCode':
                pass
                #通过 比较获取验证的请求cookies和返回的cookies是否一致 来说明 当前验证码是否有效 如果不一致 则说明上一个 session 已经失效
                #这里后期优化成 读取文件 解析验证码图片读取验证码
                keys = item.keys();
                data = {}
                #for k in keys:
                    #Env.output("{0}:{1}".format(k, item[k]))
            else:
                Env.output("pipelines else case!");
                pass            
        except Exception as ex:
            #self.log("{0}:{1} message:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, json_dumps(sys.exc_info())), logging.ERROR);
            #print "{0}:{1}  message:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno,sys.exc_info());
            
            Env.output(ex)
            Env.get_logger().error(ex)
            
            pass
        except:
            Env.output("Other Exception!")
        finally:
            pass
            return item;#最后
            
            
    def item_to_dict(self, item):
        #item转换成dict 保证 json.dumps函数能够使用
        pass
        ddict = {}
        for k in item.keys():
            ddict[k] = item[k]
            
        return ddict
        
        
class ShebaoPipeline2(object):
    pass


if __name__ == "__main__":
    obj_shebaopipe = ShebaoPipeline();
    