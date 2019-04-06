import json
from random import choice
from datetime import datetime
import jwt

from apps.users.forms import SmsCodeForm, RegisterForm, LoginForm
from apps.users.models import User
from apps.utils.AsyncYunPian import AsyncYunPian
from TornadoForum.handler import RedisHandler


class SmsHandler(RedisHandler):
    """用户注册发送验证码"""

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
        # 错误原因是因为现在传入的是一个字符串类型 不再是列表类型了
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


class RegisterHandler(RedisHandler):
    """发送短信"""

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
                # 对用户是否存在进行校验 使用 get 方法 不存在则报错
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


class LoginHandler(RedisHandler):
    """用户登录"""

    async def post(self, *args, **kwargs):
        re_data = {}

        params = self.request.body.decode("utf-8")
        params = json.loads(params)

        login_form = LoginForm.from_json(params)

        if login_form.validate():
            mobile = login_form.mobile.data
            password = login_form.password.data

            try:
                user = await self.application.objects.get(User, mobile=mobile)

                # 密码加密不可逆 将密码加密之后进行重新比较
                if user.password.check_password(password):

                    # 构建 json web token
                    # 设置过期时间要设置 UTC 时间 因为内部检查使用的也是 UTC 时间
                    payload = {
                        "id": user.id,
                        "nick_name": user.nick_name,
                        "exp": datetime.utcnow()
                    }

                    token = jwt.encode(payload, self.settings["secret_key"], algorithm='HS256')

                    re_data["id"] = user.id

                    if user.nick_name is not None:
                        re_data["nick_name"] = user.nick_name
                    else:
                        re_data["nick_name"] = user.mobile

                    re_data["token"] = token.decode("utf8")  # 将byte 类型 decode成utf-8格式

                else:

                    self.set_status(400)
                    re_data["non_fields"] = "用户名或密码错误"

            except User.DoesNotExist as e:
                self.set_status(400)
                re_data["mobile"] = "用户不存在"

            self.finish(re_data)
