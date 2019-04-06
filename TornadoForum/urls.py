"""主的URL收集文件"""

from tornado.web import url
from tornado.web import StaticFileHandler

from apps.users import urls as user_urls
from apps.community import urls as community_urls
from apps.ueditor import urls as ueditor_urls
from apps.question import urls as question_urls
from TornadoForum.settings import settings

# 配置静态文件的访问
urlpattern = [
    # 访问 media 的时候 定位到 /media 目录下
    (url("/media/(.*)", StaticFileHandler, {"path": settings["MEDIA_ROOT"]})),
]

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern

# 集成ueditor注意事项 前端的域名和后端的域名保持一致
urlpattern += ueditor_urls.urlpattern
urlpattern += question_urls.urlpattern
