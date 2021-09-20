from datetime import timedelta

from flask import Flask, render_template,session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session

app = Flask(__name__)

"""
相关配置信息
1. 数据库配置
2. redis配置: 缓存访问频率高的内容，存储session信息，图片验证码，短信验证码
3. session配置: 用来保存用户的登录信息
4. csrf配置
"""

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

app.config.from_object(Config)

# 创建SQLAlchemy对象，关联app
db = SQLAlchemy(app)

# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST,
                          port=Config.REDIS_PORT,
                          decode_responses=True) #decode_response 自解码

# 创建Session对象，读取app中session配置信息
Session(app)

@app.route('/')
def hello_world():
    # 测试redis存储数据
    redis_store.set('name','kohama')
    print(redis_store.get('name'))

    # 测试session存储
    session['name'] = 'hisae'
    print(session.get('name'))
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
