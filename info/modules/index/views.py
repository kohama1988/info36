from . import index_blue
# from ... import redis_store
from flask import current_app, render_template, session, jsonify

from ...models import User, News


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

    # 查询热门新闻，根据点击量，查询前10条
    try:
        news = News.query.order_by(News.clicks).limit(10).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno='1', errmsg='获取新闻失败')

    # 将新闻对象列表转成字典列表
    news_list = []
    for item in news:
        news_list.append(item.to_dict())

    # 取出用户信息，返回给前端
    data = {
        'user_info':user.to_dict() if user else '',
        'news': news_list
    }

    return render_template('news/index.html', data=data)

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')


