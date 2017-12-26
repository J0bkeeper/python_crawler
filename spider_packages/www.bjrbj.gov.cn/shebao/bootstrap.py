# -*- coding: utf-8 -*-

#添加的 20130317 pengzhi add
import sys
import os
import ConfigParser
import sys
#print __file__
#print sys.path
from shebao.libs.log_lib import CLog
#from shebao.libs.redis_lib import CRedis #这里会导致循环引用


#添加当前路径到模块搜索路径中
#sys.path.append(os.path.realpath(__file__))

class Env(object):        
    pass
    @classmethod
    def get_config(cls):
        #类方法 
        pass
        if not hasattr(cls, '_config'):#已经通过 _init_.py 测试 类单例模式
            config = ConfigParser.ConfigParser()
            base_path   = os.path.dirname(os.path.realpath(__file__))
            env = os.getenv('PYTHON_SHEBAO_ENV')
            if env is None: #未定义 此环境变量 则默认是 dev 线下环境配置
                env = 'dev'
            conf_file   = os.path.join(base_path, "confs/{0}.ini".format(env)) #后期考虑根据python 脚步 配置设置
            config.read(conf_file)   
            cls._config = config
           
            
        return cls._config
     
    @classmethod
    def get_logger(cls):
        pass
        if not hasattr(cls, '_logger'):
            config = ConfigParser.ConfigParser() 
            #base_path   = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            base_path   = os.path.dirname(os.path.realpath(__file__))
            env = os.getenv('PYTHON_SHEBAO_ENV')
            if env is None: #未定义 此环境变量 则默认是 dev 线下环境配置
                env = 'dev'
            conf_file   = os.path.join(base_path, "confs/{0}.ini".format(env)) #后期考虑根据python 脚步 配置设置
            config.read(conf_file)
            log_path = config.get('log', 'path')
            token    = config.get('log', 'token')
            cls._logger = CLog(log_path, token)
        return cls._logger
    
    @classmethod
    def output(cls, *args, **kwargs):
        #屏幕输出函数
        fmt = ''
        
        try:
            f = sys._getframe()
            co = f.f_code
            src_file = os.path.normcase(co.co_filename)   #当前的文件名     
            #寻找上一个文件名 和 行号
            while hasattr(f, "f_code"):
                co = f.f_code
                filename = os.path.normcase(co.co_filename) 
                if filename == src_file:
                    #print "filename:{0}".format(filename)
                    f = f.f_back
                    continue

                fmt = "{0}:{1}".format(os.path.basename(co.co_filename), f.f_lineno);
                #print "fmt {0}".format(fmt)
                break
                                
        except Exception as ex:
            print "{0}:{1} Exception:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, ex)
            fmt = 'unknow file:unknow line'
            pass        
        pass
        message = fmt;
        try:
            if len(args) > 0:
                #要求args 里面的每个参数 是字符串
                import json #ensure_ascii=False 保证中文输出正常
                message = "{0} {1}".format(message, json.dumps(args,ensure_ascii=False)) #如果元组args只有一个可变参数test 则会打印 ('test',) 格式 json.dumps(args) 则转换成[test]
            if len(kwargs) > 0:
                import json
                message = "{0} {1}".format(message, json.dumps(kwargs, ensure_ascii=False))
        except Exception as ex:
            pass
            print "Exception:{0}".format(ex);
        except:
            print "Other exception!"
        print message
    @classmethod    
    def get_redis_proxy(cls):
        from shebao.libs.redis_lib import CRedis #保证不会循环引用 
        config = ConfigParser.ConfigParser() 
        #base_path   = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        base_path   = os.path.dirname(os.path.realpath(__file__))
        
        env = os.getenv('PYTHON_SHEBAO_ENV')
        if env is None:
            env = 'dev'
        
        conf_file   = os.path.join(base_path, "confs/{0}.ini".format(env)) #后期考虑根据python 脚步 配置设置
        #print "%s:%s conf_file:%s" %(os.path.basename(__file__), sys._getframe().f_lineno, conf_file)
        config.read(conf_file)
       
        hosts = config.get('redis', 'hosts').split(",")
        port  = config.get('redis', 'port')
        timeout = config.get('redis', 'timeout')
        
        #print "get_redis_proxy :{0}".format(hosts)
        
        obj_redis_proxy = CRedis(hosts = hosts, port = port, timeout = timeout)
        return obj_redis_proxy
    
    