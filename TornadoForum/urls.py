from tornado.web import url
from tornado.web import StaticFileHandler

from apps.users import urls as user_urls
from apps.community import urls as community_urls
from TornadoForum.settings import settings

urlpattern = [
    (url("/media/(.*)", StaticFileHandler, {"path": settings["MEDIA_ROOT"]})),
]

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern
