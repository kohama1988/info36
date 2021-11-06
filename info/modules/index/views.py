from . import index_blue
# from ... import redis_store
from flask import current_app, render_template, session, jsonify, request

from ...models import User, News, Category
from sqlalchemy.sql import text

@index_blue.route('/newslist')
def newslist():
    # 获取参数
    cid = request.args.get('cid','1')
    page= request.args.get('page','1')
    per_page = request.args.get('per_page','10')

    # 参数类型转换
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        page = 1
        per_page = 10

    #分页查询
    try:
        filter = text('')
        if cid != '1':
            filter = text(News.category_id == cid)
        paginate = News.query.filter(filter).order_by(News.create_time.desc()).paginate(page, per_page, False)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno='1', errmsg='获取新闻失败')

    # 获取到分页对象中的属性，总页数，当前页，当前页的对象列表
    totalPage = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 将对象列表转换成字典列表
    news_list = []
    for news in items:
        news_list.append(news.to_dict())

    return jsonify(errno='1', errmsg='获取新闻成功',totalPage=totalPage, currentPage=currentPage, newsList=news_list)



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

    # 分类数据展示
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno='1', errmsg='获取新闻列表失败')

    category_list = []
    for item in categories:
        category_list.append(item)

    # 取出用户信息，返回给前端
    data = {
        'user_info':user.to_dict() if user else '',
        'news': news_list,
        'category': category_list
    }

    return render_template('news/index.html', data=data)

@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')


