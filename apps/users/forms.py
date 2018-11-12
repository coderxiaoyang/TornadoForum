from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

MOBILE_REGEX = "^1[358]\d{9}$|^1[48]7\d{8}$|^176\d{8}$"


class SmsCodeForm(Form):
    phone = StringField("手机号", validators=[DataRequired(message="手机号不能为空"), Regexp(MOBILE_REGEX, message="手机号不合法")])
