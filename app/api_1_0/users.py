# encoding=utf-8
from . import api
from flask import jsonify, request, current_app, url_for
from ..models.models import Post
from ..models.users import User


@api.route("/users/<int:id>")
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


# 用户关注的所有文章
@api.route("/users/<int:id>/timeline")
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for(
            "api.get_user_followed_posts", id=id, page=page - 1, _external=True
        )

    next = None
    if pagination.has_next:
        next = url_for(
            "api.get_user_followed_posts", id=id, page=page + 1, _external=True
        )

    return jsonify(
        {
            "posts": [post.to_json() for post in posts],
            "prev": prev,
            "next": next,
            "count": pagination.total,
        }
    )
