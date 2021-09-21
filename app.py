from datetime import timedelta

from flask import Flask, render_template,session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

# 创建SQLAlchemy对象，关联app
db = SQLAlchemy(app)

# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST,
                          port=Config.REDIS_PORT,
                          decode_responses=True) #decode_response 自解码

# 创建Session对象，读取app中session配置信息
Session(app)

# 使用CSRFProtect保护app
CSRFProtect(app)

@app.route('/', methods=['POST','GET'])
def hello_world():
    # 测试redis存储数据
    redis_store.set('name','kohama')
    print(redis_store.get('name'))

    # 测试session存储
    session['name'] = 'hisae'
    print(session.get('name'))
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
