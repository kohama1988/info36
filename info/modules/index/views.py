from . import index_blue
# from ... import redis_store
from flask import current_app, render_template

@index_blue.route('/', methods=['POST','GET'])
def hello_world():
    return render_template('news/index.html')

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')

