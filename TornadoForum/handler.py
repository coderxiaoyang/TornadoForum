import redis
from tornado.web import RequestHandler


# 解决跨域问题
class BaseHandler(RequestHandler):
    """
    后续使用前后端分离 我们需要在请求头中加入一个 会话id tsessionid
    因此我们需要在 Access-Control-Allow-Headers 增加这个 tsessionid
    """
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, tsessionid, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self, *args, **kwargs):
        pass


class RedisHandler(BaseHandler):
    """定义具有redis连接的handler"""

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redis_conn = redis.StrictRedis(**self.settings["redis"])
