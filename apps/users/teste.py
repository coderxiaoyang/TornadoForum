import json

import requests

web_url = "http://127.0.0.1:8800"


def test_sms():
    url = "{}/code/".format(web_url)
    data = {
        "mobile": "13707385931"
    }
    res = requests.post(url, json=data)

    print(res)

    print(json.loads(res.text))

    return json.loads(res.text)


def test_register():
    url = "{}/register/".format(web_url)
    data = {
        "mobile": "13707385931",
        "code": "0722",
        "password": "admin123"
    }
    res = requests.post(url, json=data)

    print(json.loads(res.text))
    return json.loads(res.text)


if __name__ == "__main__":
    test_sms()
    # test_register()
