from tornado.web import url

from apps.community.handler import GroupHandler, GroupMemberHandler, GroupDetailHanlder, PostHandler

urlpattern = (
    url("/groups/", GroupHandler),
    url("/groups/([0-9]+)/", GroupDetailHanlder),
    url("/groups/([0-9]+)/members/", GroupMemberHandler),

    url("/groups/([0-9]+)/posts/", PostHandler),
)
