from datetime import timedelta

from flask import Flask, render_template,session
from info import create_app, db, models

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 调用方法，获取app
app = create_app('develop')

# 创建Manager对象，管理app
manager = Manager(app)

# 使用Migrate关联app，db
Migrate(app, db)

# 给Manager添加一条操作命令
manager.add_command('db',MigrateCommand)



if __name__ == '__main__':
    manager.run()
    # app.run(host="0.0.0.0",port=5000)
