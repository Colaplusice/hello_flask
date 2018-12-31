from datetime import datetime

from flask import (
    render_template,
    jsonify,
    redirect,
    abort,
    flash,
    url_for,
    request,
    current_app,
    g,
)
from flask_login import login_required, current_user

from app import db
from app.main import forms
from app.main import main
from app.celery_tasks import export_async_posts
from app.decorators import permission_required
from app.models.models import Permission, Post, Comment
from app.main.forms import SearchForm


@main.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    post = Post.query.get_or_404(id)
    form = forms.CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data, post=post, author=current_user._get_current_object()
        )
        db.session.add(comment)
        flash("your comment has been published")
        return redirect(url_for(".post", id=post.id, page=-1))
    page = request.args.get("page", 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / current_app.config[
            "FLASKY_COMMENTS_PRE_PAGE"
        ] + 1
    pagnation = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config["FLASKY_COMMENTS_PRE_PAGE"], error_out=False
    )

    comments = pagnation.items
    return render_template(
        "post.html", post=post, form=form, comments=comments, pagination=pagnation
    )


@main.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = forms.PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash("the post have been updated")

        return redirect(url_for(".post", id=post.id))

    form.body.data = post.body
    return render_template("edit_post.html", form=form)


@main.route("/delete_article/<int:id>")
@login_required
@permission_required(Permission.DELETE_ARTICLE)
def delete_article(id):
    article = Post.query.get_or_404(id)
    print(current_user)
    if article:
        if article.author != current_user and current_user.can(Permission.ADMINISTER):
            abort(403)
        db.session.delete(article)
        flash("删除成功")
    else:
        flash("文章不存在")

    return redirect(url_for(".index"))


@main.route("/moderate")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get("page", 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config["FLASKY_COMMENTS_PRE_PAGE"], error_out=False
    )

    comments = pagination.items

    return render_template(
        "moderate.html", comments=comments, pagination=pagination, page=page
    )


@main.route("/post-article", methods=["GET", "POST"])
def post_article():
    form = forms.PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            author=current_user._get_current_object(),
        )
        # 发表文章
        db.session.add(post)
        return redirect(url_for("main.post_article"))
    return render_template("post_article.html", form=form)


@main.route("/moderate/enable/<int:id>")
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    if comment and comment.disabled:
        comment.disabled = False
        db.session.add(comment)
        # 将request传递过来的page参数再传给moderate方法
    return redirect(url_for(".moderate", page=request.args.get("page", type=int)))


@main.route("/export_posts", methods=["GET", "POST"])
@login_required
def export_posts():
    # if current_user.get_task_in_progress('export_posts'):
    #     flash('已经有一个任务在运行了，请您等一下')
    #     return redirect(url_for('main.user', username=current_user.username))
    task = export_async_posts.apply_async(args=[current_user.id])
    current_user.save_task(task.id)
    # return_msg = current_user.launch_task('export_posts', '正在导出文章...')
    # if return_msg == 'success':
    #     flash('文章正在导出，请稍等')
    # 发送邮件
    # db.session.commit()
    # else:
    #     flash('导出发生了错误..请联系管理员')
    return (
        jsonify({}),
        202,
        {"Location": url_for(".get_export_progress_status", task_id=task.id)},
    )
    # return redirect(url_for('main.user', username=current_user.username))


@main.route("/export_posts_view")
@login_required
def export_posts_view():
    return render_template("user.html", user=current_user)


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@main.route("/search")
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for("main.index"))
    page = request.args.get("page", type=int, default=1)
    print(page)
    per_page = current_app.config["POSTS_PER_PAGE"]
    posts, total = Post.search(g.search_form.q.data, page, per_page)
    next_url = (
        url_for("main.search", q=g.search_form.q.data, page=page + 1)
        if total > per_page * page
        else None
    )
    prev_url = (
        url_for("main.search", q=g.search_form.q.data, page=page - 1)
        if page > 1
        else None
    )
    return render_template(
        "search.html", title="搜索", posts=posts, next_url=next_url, pre_url=prev_url
    )
