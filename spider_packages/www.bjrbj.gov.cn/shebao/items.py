# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class ShebaoItem(scrapy.Item):
    pass
    # 基本的item类 主要包括 爬取状态 提示信息
    i_status = scrapy.Field();
    str_message = scrapy.Field();
    str_key    = scrapy.Field(); #标示某一次用户查询 通常是与时间和用户ID相关的信息
class LoginItem(ShebaoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #type:1
    #flag:3
    #j_username:340721198903232115
    #j_password:pz8316163
    #safecode:0036
    #x:43
    #y:15        
    pass
    
    #obj_response = scrapy.Field();
    i_type = scrapy.Field();#type 
    i_flag = scrapy.Field();
    str_username = scrapy.Field();
    str_password = scrapy.Field();
    str_safecode = scrapy.Field();
    i_x = scrapy.Field();
    i_y = scrapy.Field();
    dict_cookies = scrapy.Field();
    

class InfoItem(ShebaoItem):
    pass
    
    #单位名称、民族、参加工作日期、个人身份、户口性质、户口所在地、文化程度、申报月均工资收入
    kind      = scrapy.Field() #base
    unit_name = scrapy.Field()
    name      = scrapy.Field()
    nature    = scrapy.Field()
    begin_time= scrapy.Field()
    identity  = scrapy.Field()
    hkxinzhi  = scrapy.Field()
    hksuozaidi= scrapy.Field()
    whdegree = scrapy.Field()
    
   
class VerifyCodeItem(ShebaoItem):
    pass
    file_path = scrapy.Field();#图片文件路径
    str_key = scrapy.Field();
    #img_src = scrapy.Field();
    #safecode= scrapy.Field();#解析后的数字验证码
    request_cookies  = scrapy.Field()
    response_cookies = scrapy.Field();

class PayItem(scrapy.Item):
    pass
    #缴费年月、缴费基数、单位缴纳、个人缴纳、缴纳单位名称
    jfny = scrapy.Field()
    jfjs = scrapy.Field()
    dwjf = scrapy.Field()
    grjf = scrapy.Field()
    jfdw = scrapy.Field()

class OldPayItem(ShebaoItem):
    pass
    #养老保险缴费情况
    #缴费年月、缴费基数、单位缴纳、个人缴纳、缴纳单位名称
    kind = scrapy.Field() #old 养老保险
    data = scrapy.Field(serializer=str)
    #jfny = scrapy.Field()
    #jfjs = scrapy.Field()
    #dwjf = scrapy.Field()
    #grjf = scrapy.Field()
    #jfdw = scrapy.Field()
    
class MedPayItem(ShebaoItem):
    pass
    #医疗保险缴费情况
    #缴费年月、缴费基数、单位缴纳、个人缴纳、缴纳单位名称
    #jfny = scrapy.Field()
    #jfjs = scrapy.Field()
    #dwjf = scrapy.Field()
    #grjf = scrapy.Field()
    #jfdw = scrapy.Field()
    kind  = scrapy.Field()
    data  = scrapy.Field(serializer=str) #serializer=str 指明该字段的序列化函数
if  __name__ == '__main__':
    print os.path.basename(__file__);
