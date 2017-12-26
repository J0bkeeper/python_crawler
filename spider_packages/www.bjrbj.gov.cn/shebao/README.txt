#linux 使用说明
# 安装scrapy 以及相关依赖 
# 根据生产环境或者线下环境配置环境 变量 PYTHON_SHEBAO_ENV  dev|pro  如果未配置 则默认为 dev 此环境变量只影响confs中配置文件的使用
# 目前该工程主要功能是 抓取北京社保个人信息  养老保险 医疗保险信息
  1 scrapy crawl Login -a key=k1    打开登录款
  2 scrapy crawl VerifyCode -a key=k1  形成k1_safe_code.jpg 验证码图片
  3 scrapy crawl Info -a key=k1 -a username=身份证号 -a password=注册密码 -a safecode=图片验证码数值  使用第一步奏的cookie和第二步奏的验证码 登录 北京社保抓取信息 存储redis
  
#pipelines 负责存储信息 包括cookie 个人信息 社保缴费信息


#后期优化方案 
1采用 nginx 直接调用python 
2自动识别 验证码 
  