from tornado.web import url

from apps.community.handler import GroupHandler

urlpattern = (
    url("/groups/", GroupHandler),
)
