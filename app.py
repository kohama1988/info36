from datetime import timedelta

from flask import Flask, render_template,session
from info import create_app

# 调用方法，获取app
app = create_app('develop')

@app.route('/', methods=['POST','GET'])
def hello_world():
    # 测试redis存储数据
    # redis_store.set('name','kohama')
    # print(redis_store.get('name'))

    # 测试session存储
    # session['name'] = 'hisae'
    # print(session.get('name'))
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
