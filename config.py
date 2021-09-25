from datetime import timedelta
from redis import StrictRedis
import logging

"""
相关配置信息
1. 数据库配置
2. redis配置: 缓存访问频率高的内容，存储session信息，图片验证码，短信验证码
3. session配置: 用来保存用户的登录信息
4. csrf配置: 保护app，放置csrf攻击
"""

# 设置配置文件（基类配置信息）
class Config():
    DEBUG = True
    SECRET_KEY = "alkdsjfepiruijp"
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:aisin-aw23@localhost:3306/info36"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # Session配置信息
    SESSION_TYPE = 'redis' #设置session存储类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT) # 指定session存储的redis服务器
    SESSION_USE_SIGNER = True #设置签名存储
    PERMANENT_SESSION_LIFETIME = timedelta(days=2)

    #默认的日志级别
    LEVEL_NAME = logging.DEBUG

# 可以生成Config的子类，并且复写其中的属性

# 开发环境配置信息
class DevelopConfig(Config):
    pass

# 生产(线上)环境配置信息
class ProductConfig(Config):
    DEBUG = False
    LEVEL_NAME = logging.ERROR

# 测试环境配置信息
class TestConfig(Config):
    pass

# 提供一个统一的访问入口
config_dict = {
    'develop':DevelopConfig,
    'product':ProductConfig,
    'test':TestConfig
}