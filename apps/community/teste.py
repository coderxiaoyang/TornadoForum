import json
import requests

web_url = "http://127.0.0.1:8800"


def get_group():
    url = f'{web_url}/groups/'

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMTgyNDE1fQ.ovT-0td7tLcXzqC2qtY3KL6_2idYDw4OIZ1YAr9h23k'

    res = requests.get(url, headers={
        "tsessionid": token
    })

    print(res)
    print(json.loads(res.text))

    return json.loads(res.text)


if __name__ == '__main__':
    get_group()
