#coding:utf-8
import ConfigParser
import sys
import os
if '..' not in sys.path:
    sys.path.append('..')
from shebao.libs.log_lib import CLog

class Singleton(object):  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)   #返回的是一个 新对象。。。能够包含对应父类的方法
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance
    


            
     
        
       
if  __name__ == "__main__":
    import os,sys #系统已经做了重复加载处理流程 类似C++ 条件编译
    #解析配置文件测试
    config = ConfigParser.ConfigParser() 
    base_path   = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    conf_file   = os.path.join(base_path, "confs/dev.ini") #后期考虑根据python 脚步 配置设置
    print conf_file
    config.read(conf_file)   
    print config.sections()
    print config.items('log')
    #解析日志测试
    log_path = config.get('log', 'path')
    token    = config.get('log', 'token')
    logger = CLog(log_path, token)   
    #logger.info('info')
    #Env测试
    #Env.get_logger().debug('env get logger test');
    #print Env.get_logger()._findCaller()