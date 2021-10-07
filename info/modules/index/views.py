from . import index_blue
# from ... import redis_store
from info import redis_store
import logging
from flask import current_app, render_template

@index_blue.route('/', methods=['POST','GET'])
def hello_world():
    # 测试redis存储数据
    # redis_store.set('name','kohama')
    # print(redis_store.get('name'))

    # 测试session存储
    # session['name'] = 'hisae'
    # print(session.get('name'))

    # 使用日志记录方法logging进行输出可控
    logging.debug('输入调试信息')
    logging.info('输入详细信息')
    logging.warning('输入警告信息')
    logging.error('输入错误信息')

    # 使用current_app来输出日志信息
    # current_app.logger.debug('输入调试信息2')
    # current_app.logger.info('输入详细信息2')
    # current_app.logger.warning('输入警告信息2')
    # current_app.logger.error('输入错误信息2')

    return render_template('news/index.html')