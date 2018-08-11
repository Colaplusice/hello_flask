# encoding=utf-8
from . import api
from ..models.models import Post, Permisson
from .. import db
from .errors import forbidden
from .decorators import permission_required
from app.auth import auth
from flask import request, g, jsonify, url_for, current_app


@api.route('/posts/', methods=['POST'])
@permission_required(Permisson.WRITE_ARTICLES)
# 接受客户端发过来的请求
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user

    db.session.add(post)
    db.session.commit()
    return jsonify(post.tojson(), 201,
                   {'location': url_for('api.get_post', id=post.id,
                                        _external=True)})


# 更新现有资源
@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permisson.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != Post.author and \
            not g.current_user.can(Permisson.ADMINISTER):
        return forbidden("权限不够")
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    # 将post对象包装为json 再返回去
    return jsonify(post.tojson())


# 处理get请求
@api.route('/posts/')
def get_posts():
    # 从请求中得到第几页的文章
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate \
        (page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
         error_out=False)
    print(pagination.total)
    posts = pagination.items
    prev = None
    # 返回前一页的url
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page - 1, _external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page + 1, _external=True)

    return jsonify({'posts': [post.tojson() for post in posts],
                    'prev': prev,
                    'next': next,
                    'count': pagination.total
                       ,
                    })


# 返回某一篇文章
@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.tojson())
