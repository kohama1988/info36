from datetime import timedelta

from flask import Flask, render_template,session
from info import create_app

# 调用方法，获取app
app = create_app('develop')

#

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
