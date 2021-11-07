from flask import jsonify, current_app, render_template

from . import news_blue
from ...models import News


@news_blue.route('/<int:news_id>')
def news_detail(news_id):
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno='1', errmsg='获取新闻失败')

    data = {
        'news_info': news.to_dict() if news else '',
    }

    return render_template('news/detail.html', data=data)