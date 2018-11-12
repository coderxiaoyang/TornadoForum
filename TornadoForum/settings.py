import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings = {
    "static_path": "",
    "static_url_prefix": "",
    "template_path": "",
    # "secret_key": "ZGGA#Mp4yL4w5CDu",
    # "jwt_expire": 7 * 24 * 3600,
    # "MEDIA_ROOT": os.path.join(BASE_DIR, "media"),
    "SITE_URL": "http://127.0.0.1:8888",
    "db": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "love",
        "name": "message",
        "port": 3306
    },
    "redis": {
        "host": "127.0.0.1"
    }

}
