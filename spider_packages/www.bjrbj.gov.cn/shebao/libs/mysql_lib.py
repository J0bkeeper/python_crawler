#coding:utf-8
import MySQLdb
import random
#继承object 保证该类是new-style类
import sys

__author__ = 'pengzhi'
class CMysql(object):
    """ 连接MySQL数据库操作类 """
    # 三个单引号的注释 很强大 能够通过 __doc__属性返回
    #单/双下划线开头的函数或类不会被from module import *导入
    #双下划线开头的类成员函数/变量会被python内部改写，加上类名前缀。以避免与派生类同名成员冲突
    #单/双下划线都不能真正意义上阻止用户访问，只是module开发者与使用者之间的”约定”    
       
    
    _connect = False
    _conn    = None
    _cur     = None
    
    def __init__(self, hosts, port, username, password, dbname):
        #初始化函数
        self._hosts = hosts; #列表
        self._port  = port;
        self._username = username;
        self._password = password;
        self._dbname   = dbname
        self._connect  = False
        
    def connect(self):
        #初始化新建对象
        #random.shuffle(self._hosts);
        #self._connect = False;
        hosts = self._hosts[:] #深度复制
        random.shuffle(hosts)
        while (len(hosts) and False == self._connect):
            try:
                host = hosts.pop();
                #print self._hosts;
                #print "user:{0} passwd:{1} db:{2}".format(self._username, self._password, self._dbname) 
                self._conn = MySQLdb.connect(host=host,user=self._username,passwd=self._password,db=self._dbname, port=int(self._port), charset='utf8');
                #self._conn.select_db(self._dbname)
                
                self._cur = self._conn.cursor()
                self._connect = True;
                #self._cur.execute('SET NAMES utf-8');
            except MySQLdb.Error as ex:
                #print "[{0}:{1}] Exception:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, ex)
                Env.output(ex)
                Env.get_logger().error(ex)
            except Exception as ex: #所有异常 基类
                #print "[{0}:{1}] Exception:{2}".format(os.path.basename(__file__), sys._getframe().f_lineno, ex)
                Env.output(ex)
                Env.get_logger().error(ex)
            except:
                print "unknow exception"
        if False == self._connect:
            raise Exception("connect to db error !", "hosts:({0}) port:{1}".format(self._hosts, self._port));
              
        
    """execute(self, query, args)"""
    def execute(self, *args):
        pass
        iRet = 0;
        try:
            self.connect();
           
            if len(args) > 1 :
                #print "len(args):{0} args:{1}".format(len(args), args)
                sql = args[0] #元组和列表类似 只不过元组不能修改
                vals = args[1]
                iRet = self._cur.execute(sql, args) #cursor.execute("select * from writers where id = %s", "3") 预编译写法
            elif len(args) == 1:
                #print args
                #print type(args)
                sql = args[0] #元组和列表类似 只不过元组不能修改
                #print type(sql)
                #print "sql:{0}".format(sql)
                iRet = self._cur.execute(sql)
                #print self._cur.fetchone()
            else:
                raise Exception("No arg for execute!")
            
            
        except MySQLdb.Error as ex:
            print "MySQLdb.Error :{0}".format(ex)
            #args[0] 错误码 args[1] 错误提示字符串
            Env.get_logger.error(ex) #ex.args 应该是一个元组 
            Env.output(ex)
        finally:
            pass
        
        return iRet
    
    '''执行多个sql语句 只不过每个语句的参数值不同'''
    def execute_many(self, *args):
        pass
        iRet = 0;
        try:
            self.connect()
            if len(args) > 1:
                sql = args[0]
                dict_vals = args[1]
                iRet = self._cur.executemany(sql, dict_vals)
            elif len(args) == 1:
                sql = args[0]
                iRet = self._cur.executemany(sql)
            else:
                raise Exception("No arg for execute_many!")
        except MySQLdb.Error as ex:
            print ex
            Env.get_logger.error(ex)
        finally:
            pass
        return iRet;
        
    #cursor.execute("select * from writers where id = %s", "3") 预编译写法
    '''sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
       ('Mac', 'Mohan', 20, 'M', 2000)'''   
    def fetch_one(self, *args):
        pass
        self.connect()
        if len(args) > 1:
            self.execute(args[0], args[1])
        elif len(args) == 1:
            self.execute(args[0])
        else:
            raise Exception("No arg for fetch_one!")
         
        return self._cur.fetchone()
    
    def fetch_all(self, *args):
        pass
        self.connect()
        if len(args) > 1:
            self.execute(args[0], args[1]);
        elif len(args) == 1:
            self.execute(args[0]);
        else:
            raise Exception("No arg for fetch_all!")

        return self._cur.fetchall()
    
    #查询指定行数数据
    def fetch_many(self, *args, **kwargs):
        pass
        self.connect()
        if len(args) > 1:
            iRet = self.execute(args[0], args[1])
        elif len(args) == 1:
            iRet = self.execute(args[0])
        else:
            raise Exception("No arg for fetch_manay!")
        if limit is None:
            limit = 1
        return self._cur.fetchmanay(limit) #指定函数的结果急
    
    def update(self, *args):
        pass
        self.connect()
        if len(args) > 1:
            iRet = self.execute(args[0], args[1])
        elif len(args) == 1:
            iRet = self.execute(args[0])
        else:
            raise Exception("No arg for update!")
        
        return iRet;
        
    #析构函数
    def __del__(self):
        pass
        try:
            self.close()
        except Exception as ex:
            Env.output(ex)
            Env.get_logger.error(ex)
    
        
    def begin(self):
        pass
        return self.connect()
    def commit(self):
        pass
        return self._conn.commit()
    
    def rollback(self):
        pass
        return self._conn.rollback()
    
    def getLastInsertId(self):
        return self._cur.lastrowid
    
    def rowcount(self):
        return self._cur.rowcount
    
    def close(self):
        self._cur.close()
        self._conn.close()
        
        
if __name__ == '__main__':
    #测试
    try:
        import sys
        print sys.path
        if '..' not in sys.path:
            sys.path.append('..')
        import ConfigParser
        import os
        config = ConfigParser.ConfigParser();
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        conf_file = os.path.join(base_path, "confs/dev.ini")
        print conf_file
        print config.read(conf_file) #返回读取的文件 全路径 conf_file 列表
        
        hosts =   config.get('db', 'hosts').split(",")
        print hosts
        print type(hosts) #str,str 字符串类型(123...,113)
        port  = config.get('db', 'port')
        username = config.get('db', 'username')
        password = config.get('db', 'password')
        dbname   = config.get('db', 'dbname')
        obj_mysql = CMysql(hosts = hosts, port = port, username = username, password = password, dbname = dbname)
        obj_mysql.connect()
        tuple_row =  obj_mysql.fetch_one('select * from `user`')
        for val in tuple_row:
            print val
    except Exception as ex:
        print "Exception :{0}".format(ex)
    
    