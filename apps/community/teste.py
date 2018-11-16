import json
import requests

web_url = "http://127.0.0.1:8800"


def get_group():
    url = f'{web_url}/groups/'

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMjYyOTk5fQ._CyxwhZi--rFbIR6KQg-daGLlfMLqaoWRoj1q29CKoQ'
    res = requests.get(url, headers={
        "tsessionid": token
    })

    print(res)
    print(json.loads(res.text))

    return json.loads(res.text)


def create_group():
    url = f'{web_url}/groups/'

    # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMjYyOTk5fQ._CyxwhZi--rFbIR6KQg-daGLlfMLqaoWRoj1q29CKoQ'

    token = ''

    files = {
        "front_image": open('/Users/Downloads/luntuan/flash.jpg', 'rb')
    }

    data = {
        "name": "闪电侠",
        "desc": "这里是DC家的小闪讨论组！",
        "notice": "希望你像小闪一样是个话痨",
        "category": "DC宇宙"
    }

    res = requests.post(url, headers={
        "tsessionid": token
    }, data=data, files=files)

    print(res.status_code)
    print(json.loads(res.text))

    return json.loads(res.text)


def apply_group(group_id, apply_reason):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMjYyOTk5fQ._CyxwhZi--rFbIR6KQg-daGLlfMLqaoWRoj1q29CKoQ'

    headers = {
        "tsessionid": token
    }
    apply_reason = "测试一下"
    data = {
        "apply_reason": apply_reason,
    }
    res = requests.post(f"{web_url}/groups/{group_id}/members/", headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))
    return json.loads(res.text)


def get_group_detail(group_id):

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMjYyOTk5fQ._CyxwhZi--rFbIR6KQg-daGLlfMLqaoWRoj1q29CKoQ'

    headers = {
        "tsessionid": token
    }

    res = requests.get(f"{web_url}/groups/{group_id}/", headers=headers)
    print(res.status_code)
    print(json.loads(res.text))
    return json.loads(res.text)


def add_post(group_id):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMjYyOTk5fQ._CyxwhZi--rFbIR6KQg-daGLlfMLqaoWRoj1q29CKoQ'

    headers = {
        "tsessionid": token
    }

    data = {
        "title": "小孩子不要看漫画",
        "content": "小孩子不要看漫画",
    }
    res = requests.post(f"{web_url}/groups/{group_id}/posts/", headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))
    return json.loads(res.text)


def get_post_detail(post_id):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMjYyOTk5fQ._CyxwhZi--rFbIR6KQg-daGLlfMLqaoWRoj1q29CKoQ'

    headers = {
        "tsessionid": token
    }

    res = requests.get(f"{web_url}/posts/{post_id}/", headers=headers)
    print(res.status_code)
    print(json.loads(res.text))
    return json.loads(res.text)


def add_comment(post_id):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmlja19uYW1lIjoiXHU3ZWEyXHU3MGU3XHU4MDg5IiwiZXhwIjoxNTQyMjYyOTk5fQ._CyxwhZi--rFbIR6KQg-daGLlfMLqaoWRoj1q29CKoQ'

    headers = {
        "tsessionid": token
    }

    data = {
        "content": "小孩子不要看漫画",
    }
    res = requests.post(f"{web_url}/posts/{post_id}/comments/", headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))

    return json.loads(res.text)


if __name__ == '__main__':
    # get_group()

    # create_group()

    # apply_group(7, "测试一下")
    # get_group_detail(7)
    # add_post(7)
    # get_post_detail(1)
    add_comment(1)

    pass
