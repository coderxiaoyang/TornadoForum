from tornado.web import url

from apps.community.handler import (GroupHandler, GroupMemberHandler, GroupDetailHanlder, PostHandler,
                                    PostDetailHandler, PostCommentHanlder, CommentReplyHandler, CommentsLikeHanlder)

urlpattern = (
    url("/groups/", GroupHandler),
    url("/groups/([0-9]+)/", GroupDetailHanlder),
    url("/groups/([0-9]+)/members/", GroupMemberHandler),

    url("/groups/([0-9]+)/posts/", PostHandler),

    url("/posts/([0-9]+)/", PostDetailHandler),
    # 评论帖子
    url("/posts/([0-9]+)/comments/", PostCommentHanlder),
    # 回复评论
    url("/comments/([0-9]+)/replys/", CommentReplyHandler),
    # 点赞数
    url("/comments/([0-9]+)/likes/", CommentsLikeHanlder),
)
