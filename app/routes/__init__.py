# app/routes/__init__.py

from flask import Blueprint

# 创建一个名为 'routes' 的 Blueprint 对象
routes = Blueprint('routes', __name__)

# 导入具体的路由模块，并注册到 Blueprint 对象上
from app.routes.stock import *
# 导入其他路由模块并注册...

# 在这里可以继续导入和注册其他路由模块

# 最后，将 Blueprint 对象注册到 app 中
from app import app
app.register_blueprint(routes)