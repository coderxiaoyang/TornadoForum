import json
import os
import uuid

import aiofiles
from playhouse.shortcuts import model_to_dict

from TornadoForum.handler import RedisHandler
from apps.question.forms import QuestionForm, AnswerForm, AnswerReplyForm
from apps.question.models import Question, Answer
from apps.users.models import User
from apps.utils.auth_decorators import authenticated_async
from apps.utils.utils_func import json_serial


class QuestionHandler(RedisHandler):

    async def get(self, *args, **kwargs):
        re_data = []
        question_query = Question.extend()

        c = self.get_argument("c", None)
        if c:
            question_query = question_query.filter(Question.category == c)

        order = self.get_argument("o", None)
        if order:
            if order == "new":
                question_query = question_query.order_by(Question.add_time.desc())
            elif order == "hot":
                question_query = question_query.order_by(Question.answer_nums.desc())

        questions = await self.application.objects.execute(question_query)
        for question in questions:
            question_dict = model_to_dict(question)
            question_dict["image"] = "{}/media/{}/".format(self.settings["SITE_URL"], question_dict["image"])
            re_data.append(question_dict)

            self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, *args, **kwargs):
        # 添加问题
        re_data = {}

        question_form = QuestionForm(self.request.body_arguments)
        if question_form.validate():
            # 自己完成图片字段的验证
            files_meta = self.request.files.get("image", None)
            if not files_meta:
                self.set_status(400)
                re_data["image"] = "请上传图片"
            else:
                # 完成图片保存并将值设置给对应的记录
                # 通过aiofiles写文件
                # 1. 文件名
                new_filename = ""
                for meta in files_meta:
                    filename = meta["filename"]
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    file_path = os.path.join(self.settings["MEDIA_ROOT"], new_filename)
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(meta['body'])

                question = await self.application.objects.create(Question,
                                                                 user=self.current_user,
                                                                 category=question_form.category.data,
                                                                 title=question_form.title.data,
                                                                 content=question_form.content.data,
                                                                 image=new_filename)
                re_data["id"] = question.id
        else:
            self.set_status(400)
            for field in question_form.errors:
                re_data[field] = question_form.errors[field][0]

        self.finish(re_data)


class QuestionDetailHandler(RedisHandler):
    """问题的详情"""

    async def get(self, question_id, *args, **kwargs):
        re_data = {}
        question_details = await self.application.objects.execute(
            Question.extend().where(Question.id == int(question_id)))
        re_count = 0
        for data in question_details:
            item_dict = model_to_dict(data)
            item_dict["image"] = "{}/media/{}/".format(self.settings["SITE_URL"], item_dict["image"])
            re_data = item_dict
            re_count += 1

        if re_count == 0:
            self.set_status(404)

        self.finish(json.dumps(re_data, default=json_serial))


class AnswerHanlder(RedisHandler):
    # @authenticated_async
    async def get(self, question_id, *args, **kwargs):
        # 获取问题的的所有回答
        re_data = []

        try:
            question = await self.application.objects.get(Question, id=int(question_id))
            answsers = await self.application.objects.execute(
                Answer.extend().where(Answer.question == question, Answer.parent_answer.is_null(True)).order_by(
                    Answer.add_time.desc())
            )

            for item in answsers:
                item_dict = {
                    "user": model_to_dict(item.user),
                    "content": item.content,
                    "reply_nums": item.reply_nums,
                    "id": item.id,
                }

                re_data.append(item_dict)
        except Question.DoesNotExist as e:
            self.set_status(404)
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, question_id, *args, **kwargs):
        # 新增评论
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = AnswerForm.from_json(param)
        if form.validate():
            try:
                question = await self.application.objects.get(Question, id=int(question_id))
                answer = await self.application.objects.create(Answer, user=self.current_user, question=question,
                                                               content=form.content.data)
                question.answer_nums += 1
                await self.application.objects.update(question)
                re_data["id"] = answer.id
                re_data["user"] = {
                    "nick_name": self.current_user.nick_name,
                    "id": self.current_user.id
                }
            except Question.DoesNotExist as e:
                self.set_status(404)
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]

        self.finish(re_data)


class AnswerReplyHandler(RedisHandler):

    @authenticated_async
    async def get(self, answer_id, *args, **kwargs):
        re_data = []
        answer_replys = await self.application.objects.execute(
            Answer.extend().where(Answer.parent_answer_id == int(answer_id)))

        for item in answer_replys:
            item_dict = {
                "user": model_to_dict(item.user),
                "content": item.content,
                "reply_nums": item.reply_nums,
                "add_time": item.add_time.strftime("%Y-%m-%d"),
                "id": item.id
            }

            re_data.append(item_dict)

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, answer_id, *args, **kwargs):
        # 添加回复
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = AnswerReplyForm.from_json(param)
        if form.validate():
            try:
                answer = await self.application.objects.get(Answer, id=int(answer_id))
                replyed_user = await self.application.objects.get(User, id=form.replyed_user.data)

                reply = await self.application.objects.create(Answer, user=self.current_user, parent_answer=answer,
                                                              reply_user=replyed_user, content=form.content.data)

                # 修改comment的回复数
                answer.reply_nums += 1
                await self.application.objects.update(answer)

                re_data["id"] = reply.id
                re_data["user"] = {
                    "id": self.current_user.id,
                    "nick_name": self.current_user.nick_name
                }

            except Answer.DoesNotExist as e:
                self.set_status(404)
            except User.DoesNotExist as e:
                self.set_status(400)
                re_data["replyed_user"] = "用户不存在"
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]

        self.finish(re_data)
