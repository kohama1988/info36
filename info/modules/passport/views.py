from . import passport_blue
from info.utils.captcha.captcha import captcha
from flask import request, current_app, make_response

from ... import redis_store, constants


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
