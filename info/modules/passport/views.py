import json

from . import passport_blue
from info.utils.captcha.captcha import captcha
from flask import request, current_app, make_response, jsonify, session

from ... import redis_store, constants, db
from ...models import User


@passport_blue.route('/image_code')
def image_code():

    # 获取前端传递的参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')

    # 获取图片
    name, text, image_data = captcha.generate_captcha()

    # 将图片验证码的值保存到redis
    try:
        redis_store.set('image_code:{}'.format(cur_id), text, constants.IMAGE_CODE_REDIS_EXPIRES )

        if pre_id:
            redis_store.delete('image_code:{}'.format(pre_id))
    except Exception as e:
        current_app.logger.error(e)
        return '图片验证码操作失败'
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@passport_blue.route('/register', methods=['POST'])
def register():
    # 获取数据
    # json_data = request.data
    # dict_data = json.loads(json_data)
    dict_data = request.json # request.get_json()效果是一样的
    mobile = dict_data.get('mobile')
    password = dict_data.get('password')

    # 校验参数
    if not all([mobile, password]):
        return jsonify(errno='1', errmsg='参数不全')

    # 创建用户对象
    user = User()
    user.nick_name = mobile
    user.password = password
    user.mobile = mobile
    user.signature = "该用户很懒，什么也没写"

    # 保存用户到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno='1', errmsg="注册失败")
    return jsonify(errno='0', errmsg="注册成功")

@passport_blue.route('/login', methods=['POST'])
def login():
    # 获取数据
    dict_data = request.json
    mobile = dict_data.get('mobile')
    password = dict_data.get('password')

    # 校验数据
    if not all([mobile, password]):
        return jsonify(errno='1', errmsg='参数不全')

    # 通过手机号，到数据库查询用户对象
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno='1', errmsg='未找到该用户')

    # 判断用户是否存在
    if not user:
        return jsonify(errno='1', errmsg='该用户不存在')

    if not user.check_passowrd(password):
        return jsonify(errno='1', errmsg='密码错误')

    # 将用户的登录信息保存到session中
    session['user_id'] = user.id

    return jsonify(errno='0', errmsg='登录成功')
