from flask import (
    render_template,
    jsonify,
    redirect,
    abort,
    flash,
    url_for,
    request,
    current_app,
)
from flask_login import login_required, current_user

from app import db
from .. import forms
from .. import main
from ...celery_tasks import export_async_posts
from ...decorators import permission_required
from ...models import Permisson, Post, Comment


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
    if current_user != post.author and not current_user.can(Permisson.ADMINISTER):
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
@permission_required(Permisson.DELETE_ARTICLE)
def delete_article(id):
    article = Post.query.get_or_404(id)
    print(current_user)
    if article:
        if article.author != current_user and current_user.can(Permisson.ADMINISTER):
            abort(403)
        db.session.delete(article)
        flash("删除成功")
    else:
        flash("文章不存在")

    return redirect(url_for(".index"))


@main.route("/moderate")
@login_required
@permission_required(Permisson.MODERATE_COMMENTS)
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
    if current_user.can(Permisson.WRITE_ARTICLES) and form.validate_on_submit():
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
@permission_required(Permisson.MODERATE_COMMENTS)
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