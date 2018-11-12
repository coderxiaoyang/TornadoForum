from tornado.web import url

from apps.users.handler import SmsHandler

urlpattern = (
    url('/code/', SmsHandler),
)
