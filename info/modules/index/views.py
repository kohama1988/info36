from . import index_blue
# from ... import redis_store
from flask import current_app, render_template, session

from ...models import User


@index_blue.route('/', methods=['POST','GET'])
def hello_world():

    # 获取用户的登录信息
    user_id = session.get('user_id')

    # 通过用户的ID取出用户信息
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 取出用户信息，返回给前端
    data = {
        'user_info':user.to_dict() if user else ''
    }

    return render_template('news/index.html', data=data)

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')

