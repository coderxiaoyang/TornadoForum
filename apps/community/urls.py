from tornado.web import url

from apps.community.handler import GroupHandler, GroupMemberHandler, GroupDetailHanlder

urlpattern = (
    url("/groups/", GroupHandler),
    url("/groups/([0-9]+)/", GroupDetailHanlder),
    url("/groups/([0-9]+)/members/", GroupMemberHandler),
)
