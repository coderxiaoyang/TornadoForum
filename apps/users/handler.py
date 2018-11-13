import json
from random import choice

from apps.users.forms import SmsCodeForm, RegisterForm
from apps.users.models import User
from apps.utils.AsyncYunPian import AsyncYunPian
from TornadoForum.handler import RedisHandler


class RegisterHandler(RedisHandler):

    async def post(self, *args, **kwargs):

        re_data = {}

        params = self.request.body.decode('utf-8')
        params = json.loads(params)

        register_form = RegisterForm.from_json(params)

        if register_form.validate():
            # 取出相关数据
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data

            # 校验验证码
            redis_key = f'{mobile}_{code}'

            if self.redis_conn.get(redis_key):
                # 对用户是否存在进行校验
                try:
                    existed_user = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    re_data["mobile"] = "用户已存在"

                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    re_data["id"] = user.id

            else:

                self.set_status(400)
                re_data['code'] = '验证码错误或者已失效！'

        else:
            self.set_status(400)
            for field in register_form.errors:
                re_data[field] = register_form.errors[field][0]

        self.finish(re_data)


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
            mobile = sms_form.mobile.data

            yun_pian = AsyncYunPian("7b14af96096b7f9f12ed467d21102fab")
            res_json = await yun_pian.send_single_sms(code, mobile)

            if res_json["code"] != 0:
                self.set_status(400)
                re_data["mobile"] = res_json["msg"]

            else:
                # 将验证码和手机号作为键存储到 redis 设置过期时间十分钟
                self.redis_conn.set(f"{mobile}_{code}", 1, 10 * 60)

        else:

            self.set_status(400)

            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]

        self.finish(re_data)
