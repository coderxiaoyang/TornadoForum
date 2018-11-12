# -*- coding: utf-8 -*-

"""主程序"""

from tornado import web, ioloop
# from peewee_async import Manager
import wtforms_json

from TornadoForum.urls import urlpattern
from TornadoForum.settings import settings

if __name__ == '__main__':
    # 集成json到wtforms
    wtforms_json.init()

    app = web.Application(
        urlpattern, debug=True, **settings
    )

    # objects = Manager(database)

    app.listen(8888)

    ioloop.IOLoop.current().start()

