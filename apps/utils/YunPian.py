# -*- coding: utf-8 -*-

"""使用云片网进行短信发送"""

import requests


class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_single_sms(self, code, mobile):
        # 发送单条短信
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【慕课实战】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        res = requests.post(url, data={
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        })

        return res


if __name__ == "__main__":
    # api_key 可以在主页找到
    yun_pian = YunPian("7b14af96096b7f9f0ced427d21822fa1")
    res = yun_pian.send_single_sms("1234", "13788765321")
    print(res.text)
