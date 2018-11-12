# -*- coding: utf-8 -*-

"""异步发送短信"""

import json
from urllib.parse import urlencode
from functools import partial

from tornado import ioloop, httpclient


class AsyncYunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    async def send_single_sms(self, code, mobile):
        # 只有在协程中才能去使用另外一个协程

        http_client = httpclient.AsyncHTTPClient()

        url = "http://sms.yunpian.com/v2/sms/single_send.json"
        text = "【慕课实战】您的验证码是{}。如非本人操作，请忽略本短信".format(code)

        # 使用 HTTPRequest 构建请求
        # 使用 urlencode 将参数进行编码下
        post_request = httpclient.HTTPRequest(url=url, method="POST", body=urlencode({
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        }))

        res = await http_client.fetch(post_request)
        return json.loads(res.body.decode("utf8"))


if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()

    yun_pian = AsyncYunPian("7b14af96096b7f9f0ced461112822fab")

    # 通过 partial 可以将带参数的函数重新组装成一个函数
    new_func = partial(yun_pian.send_single_sms, "1234", "13788765423")

    # run_sync方法可以在运行完某个协程之后停止事件循环
    io_loop.run_sync(new_func)
