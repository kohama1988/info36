from flask import Blueprint

# 创建蓝图对象
index_blue = Blueprint('index',__name__)

# 导入views文件装饰视图函数
# from info.modules.index import views
from . import views
# .表示当前模块

