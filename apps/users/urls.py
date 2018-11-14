from tornado.web import url

from apps.users.handler import SmsHandler, RegisterHandler, LoginHandler

urlpattern = (
    url('/code/', SmsHandler),
    url('/register/', RegisterHandler),
    url('/login/', LoginHandler),
)
