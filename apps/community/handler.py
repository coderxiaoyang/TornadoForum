import os
import uuid

import aiofiles

from TornadoForum.handler import RedisHandler
from apps.utils.auth_decorators import authenticated_async
from apps.community.forms import CommunityGroupForm
from apps.community.models import CommunityGroup, CommunityGroupMember


class GroupHandler(RedisHandler):

    async def get(self, *args, **kwargs):
        self.finish({
            "code": 100
        })

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}

        # 传输方式是表单提交不再是json格式
        community_form = CommunityGroupForm(self.request.body_arguments)

        if community_form.validate():
            # 这里我们自己校验文件传输
            file_meta = self.request.files.get("front_image", None)

            if file_meta:
                # 文件存在的话就要设置保存 文件的读写和 socket 一样都是 IO 操作 因此这个地方我们需要异步操作

                for meta in file_meta:
                    filename = meta["filename"]
                    # 为了防止重复文件名 保存的时候覆盖 为上传的文件重新命名
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    file_path = os.path.join(self.settings["MEDIA_ROOT"], new_filename)

                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(meta['body'])

                    group = await self.application.objects.create(CommunityGroup,
                                                                  add_user=self.current_user,
                                                                  name=community_form.name.data,
                                                                  category=community_form.category.data,
                                                                  desc=community_form.desc.data,
                                                                  notice=community_form.notice.data,
                                                                  front_image=new_filename)
                    re_data["id"] = group.id

            else:
                self.set_status(400)
                re_data["front_image"] = "请上传图片!"

        else:
            self.set_status(400)
            for field in community_form.errors:
                re_data[field] = community_form.errors[field][0]

        self.finish(re_data)
