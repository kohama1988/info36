from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect, generate_csrf
from config import config_dict
import logging

# 定义redis_store变量
from info.utils.commons import hot_news_filter

redis_store = None

# 定义数据库文件
db = SQLAlchemy()

# 定义工厂方法
def create_app(config_name):

    app = Flask(__name__)

    # 根据传入的配置类名称，取出相应的配置类
    config = config_dict.get(config_name)

    # 调用日志方法，记录程序运行的信息
    log_file(config.LEVEL_NAME)

    app.config.from_object(config)

    # 创建SQLAlchemy对象，关联app
    db.init_app(app)

    # 创建redis对象
    global redis_store
    redis_store = StrictRedis(host=config.REDIS_HOST,
                              port=config.REDIS_PORT,
                              decode_responses=True) #decode_response 自解码

    # 创建Session对象，读取app中session配置信息
    Session(app)

    # 使用CSRFProtect保护app
    """
    使用ajax提交时
     - 在cookie中设置csrf_token（自己写）
     - 在请求头中设置csrf_token（自己写）
     - 服务器： 取出2者进行校验
    """
    CSRFProtect(app)

    # 将首页蓝图index_blue注册到app中
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)

    from info.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    from info.modules.news import news_blue
    app.register_blueprint(news_blue)
    # 将函数添加到默认过滤器列表
    app.add_template_filter(hot_news_filter,'my_filter')

    # 使用请求钩子拦截所有的请求，通过的在cookie中设置csrf_token
    @app.after_request
    def after_request(resp):
        csrf_token = generate_csrf()
        resp.set_cookie('csrf_token',csrf_token)
        return resp

    print(app.url_map)
    return app

def log_file(LEVEL_NAME):
    # 设置日志的记录等级， DEBUG<INFO<WARNING<ERROR
    logging.basicConfig(level=LEVEL_NAME)
    # 创建日志记录器，知名日志保存的路径，每个日志文件的大小，保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log',maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式，日志等级，输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)