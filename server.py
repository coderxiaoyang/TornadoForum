# -*- coding: utf-8 -*-

"""主程序"""

from tornado import web, ioloop
from peewee_async import Manager
import wtforms_json

from TornadoForum.urls import urlpattern
from TornadoForum.settings import settings, database

if __name__ == '__main__':
    # 集成json到wtforms
    wtforms_json.init()

    app = web.Application(
        urlpattern, debug=True, **settings
    )

    # 设置数据库管理对象 objects
    objects = Manager(database)
    database.set_allow_sync(False)
    app.objects = objects

    app.listen(8800)

    ioloop.IOLoop.current().start()

