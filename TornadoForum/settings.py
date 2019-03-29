"""配置文件"""

import os

import peewee_async

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings = {
    "static_path": "",
    "static_url_prefix": "",
    "template_path": "",
    "secret_key": "gk@vjv5!qwS4HneD",
    "jwt_expire": 7 * 24 * 3600,
    "MEDIA_ROOT": os.path.join(BASE_DIR, "media"),
    "SITE_URL": "http://127.0.0.1:8800",
    "db": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "love",
        "name": "forum",
        "port": 3306
    },
    "redis": {
        "host": "127.0.0.1"
    }

}

database = peewee_async.MySQLDatabase(
    'forum', host="127.0.0.1", port=3306, user="root", password="love"
)
