from tornado.web import url

from apps.users.handler import SmsHandler, RegisterHandler

urlpattern = (
    url('/code/', SmsHandler),
    url('/register/', RegisterHandler),
)
