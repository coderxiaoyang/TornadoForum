from tornado.web import authenticated

from TornadoForum.handler import RedisHandler
from apps.utils.auth_decorators import authenticated_async


class GroupHandler(RedisHandler):

    @authenticated_async
    async def get(self, *args, **kwargs):
        self.finish({
            "code": 100
        })
