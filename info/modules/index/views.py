from . import index_blue
# from ... import redis_store
from info import redis_store

@index_blue.route('/', methods=['POST','GET'])
def hello_world():
    # 测试redis存储数据
    redis_store.set('name','kohama')
    print(redis_store.get('name'))

    # 测试session存储
    # session['name'] = 'hisae'
    # print(session.get('name'))
    return 'Hello World!'