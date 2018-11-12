import redis
from tornado.web import RequestHandler


class RedisHandler(RequestHandler):
    """定义具有redis连接的handler"""

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redis_conn = redis.StrictRedis(**self.settings["redis"])

