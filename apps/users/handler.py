import json
from random import choice

from apps.users.forms import SmsCodeForm
from apps.utils.AsyncYunPian import AsyncYunPian
from TornadoForum.handler import RedisHandler


class SmsHandler(RedisHandler):

    # 生成随机的验证码
    def get_code(self):
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    async def post(self, *args, **kwargs):

        re_data = {}

        params = self.request.body.decode('utf-8')
        params = json.loads(params)

        # 使用 wtforms_json 打猴子补丁 解决参数格式化错误问题
        sms_form = SmsCodeForm.from_json(params)

        if sms_form.validate():
            code = self.get_code()
            phone = sms_form.phone.data

            yun_pian = AsyncYunPian("7b14af96096b7f9f0c12467d21822fab")
            res_json = await yun_pian.send_single_sms(code, phone)

            if res_json["code"] != 0:
                self.set_status(400)
                re_data["phone"] = res_json["msg"]

            else:
                # 将验证码和手机号作为键存储到 redis 设置过期时间十分钟
                self.redis_conn.set(f"{phone}_{code}", 1, 10 * 60)

        else:

            self.set_status(400)

            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]

        self.finish(re_data)
