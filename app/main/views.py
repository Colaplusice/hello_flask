# encoding=utf-8
import os
from flask import render_template, jsonify, redirect, abort, flash, \
    make_response, url_for, request, current_app
from app import db
from hello_flask import app
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import forms
from . import main
import datetime
from ..decorators import amdin_required, permission_required
# from ..models import
from ..models.Page_view import View_message, User_message
from ..models.Users import User
from ..models.Role import Role
from ..models.models import Permisson, Post, Comment, Message, Notification


# 设置cookie为0 然后跳转到Index页面
@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


# 设置为1，保存用户默认习惯
@main.route('/show_followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.before_app_request
def get_user_message():
    if request.url_rule.endpoint != 'static':
        view_data = {
            'url': request.url,
            'ip': request.remote_addr,
            'referrer': request.referrer,
            'req_method': request.method,
            'end_point': request.url_rule.endpoint,
            'user_agent': request.user_agent
        }
        user_data = {
            'ip': request.remote_addr
        }
        User_message.create_or_update_from_request(user_data)
        View_message.create_from_request(view_data)


@main.route('/moderate')
@login_required
@permission_required(Permisson.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    # 提取一页评论 吧把分页对象也传入html
    pagination = Comment.query.order_by(Comment.timestamp.desc()) \
        .paginate(page,
                  per_page=current_app.config['FLASKY_COMMENTS_PRE_PAGE'],
                  error_out=False
                  )

    comments = pagination.items

    return render_template(
        'moderate.html', comments=comments, pagination=pagination,
        page=page)


@main.after_app_request
def after_request(response):
    print(response)
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                '缓慢的语句:%s\n 参数:%s\n 持续时长:%fs\n,内容:%s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context)
            )
    return response


@main.route('/post-article', methods=['GET', 'POST'])
def post_article():
    form = forms.PostForm()
    if current_user.can(Permisson.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        # 发表文章
        db.session.add(post)
        return redirect(url_for('main.post_article'))
    return render_template('post_article.html', form=form)


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    show_followed = False
    # 从cookie获得默认值
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        print('show follow')
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return_msg = render_template(
        'index.html',
        posts=posts,
        pagination=pagination
    )

    return return_msg


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = forms.CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('your comment has been published')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
               current_app.config['FLASKY_COMMENTS_PRE_PAGE'] + 1
    pagnation = post.comments.order_by(Comment.timestamp.asc()) \
        .paginate(page,
                  per_page=current_app.config['FLASKY_COMMENTS_PRE_PAGE'],
                  error_out=False
                  )

    comments = pagnation.items
    return render_template('post.html',
                           post=post,
                           form=form,
                           comments=comments,
                           pagination=pagnation
                           )


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permisson.ADMINISTER):
        abort(403)
    form = forms.PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('the post have been updated')

        return redirect(override_url_for('.post', id=post.id))

    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    pass


# 关注user用户
@main.route('/follow/<username>')
@login_required
@permission_required(Permisson.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for('.index'))

    if current_user.is_following(user):
        flash("you have already following user")

        return redirect(url_for('.user', username=username))

    current_user.follow(user)
    flash('you are now following the user%s.' % username)
    return redirect(url_for('.user', username=username))


# 返回用户的所有关注者
@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("invalid user")
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)

    pagination = user.follower.paginate(
        page, per_page=current_app.config['FLASKY_USER_PER_PAGE'],
        error_out=False
    )
    follows = [{'user': item.follower, 'timestamp': item.timestamp
                } for item in pagination.items]
    return render_template('followers.html',
                           user=user, title='Followers of',
                           endpoint='.followers',
                           pagination=pagination,
                           follows=follows)


# username关注的用户
@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user')
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=current_app.config[
        'FLASKY_USER_PER_PAGE'],
                                        error_out=False)

    followed = [{'user': item.followed, 'timestamp': item.timestamp}
                for item in pagination.items]

    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by',
                           pagination=pagination, follows=followed)


@login_required
@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    edit_form = forms.UserEditForm()
    if edit_form.validate_on_submit():
        current_user.name = edit_form.name.data
        current_user.location = edit_form.location.data
        current_user.about_me = edit_form.about_me.data
        db.session.add(current_user)
        flash('your data has been updated')

    edit_form.about_me.data = current_user.about_me
    edit_form.location.data = current_user.location
    edit_form.name.data = current_user.name
    # 处理get数据
    return render_template('edit_profile.html', form=edit_form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@amdin_required
def edit_profile_admin(id):
    # 通过主键得到
    user = User.query.get_or_404(id)
    form = forms.EditProfileAdminForm(user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confrimed.data
        if Role.query.filter_by(name=form.role.data).first:
            user.role = Role.query.filter_by(name=form.role.data).first()
        user.name = form.name.data
        user.about_me = form.about_me.data
        user.location = form.location.data
        db.session.add(user)
        flash('个人信息更新成功')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.name.data = user.name
    form.about_me.data = user.about_me
    form.location.data = user.location
    form.role.data = user.role
    form.confrimed.data = user.confirmed

    return render_template('edit_profile.html', form=form, user=user)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permisson.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    if comment and comment.disabled:
        comment.disabled = False
        db.session.add(comment)
        # 将request传递过来的page参数再传给moderate方法
    return redirect(
        url_for('.moderate', page=request.args.get('page', type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permisson.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    if comment and not comment.disabled:
        comment.disabled = True
        db.session.add(comment)
    return redirect(
        url_for('.moderate', page=request.args.get('page', type=int)))


@main.route('/delete_article/<int:id>')
@login_required
@permission_required(Permisson.DELETE_ARTICLE)
def delete_article(id):
    article = Post.query.get_or_404(id)
    print(current_user)
    if article:
        if article.author != current_user and current_user.can(
                Permisson.ADMINISTER):
            abort(403)
        db.session.delete(article)
        flash('删除成功')
    else:
        flash('文章不存在')

    return redirect(url_for('.index'))


@main.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash('已经有一个任务在运行了，请您等一下')
        return redirect(url_for('main.user', username=current_user.username))
    else:
        # 添加到任务队列来完成，所以是异步的
        return_msg = current_user.launch_task('export_posts', '正在导出文章...')
        if return_msg == 'success':
            flash('文章正在导出，请稍等')
            db.session.commit()
        else:
            flash('导出发生了错误..请联系管理员')
        return redirect(url_for('main.user', username=current_user.username))


@main.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
# 唯一username
def send_message(recipient):
    receive_user = User.query.filter_by(username=recipient).first_or_404()

    # 会自动从request中加载MessageForm
    form = forms.MessageForm()

    if form.validate_on_submit():
        message = Message(author=current_user, recipient=receive_user,
                          body=form.message.data)
        # 将new_messages函数的返回值传递给add_notification方法 是一个数字
        receive_user.add_notification('未读的消息数', receive_user.new_messages())
        db.session.add(message)
        db.session.commit()
        flash('你的消息已经发送给了{}'.format(receive_user.username))
    return render_template('send_messages.html', title='发送消息',
                           form=form, recipient=recipient)


@main.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    # 更新未读的消息数
    current_user.add_notification('未读的消息数', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
        page, current_app.config['FLASKY_USER_PER_PAGE'], False
    )
    next_url = url_for('.messages', page=messages.next_num) \
        if messages.has_next else None

    pre_url = url_for('.messages', page=messages.prev_num) \
        if messages.has_prev else None

    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, pre_url=pre_url)


# 某个时间点以后的通知 时间包含在请求中
@main.route('/notifications')
@login_required
def notifications():
    # since = request.args.get('since', 0.0, type=float)
    # asc升序
    notifications = current_user.notifications.filter_by(
        Notification.timestamp.asc())

    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications
    ])


@app.context_processor
def override_url_for():
    print('override the url_for method')
    return dict(url_for=dated_url_for)


# 给values dict 新增加了个 timestamp
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = (os.path.join(app.root_path, endpoint, filename))
            values['q'] = int(os.stat(file_path).st_atime)

    return url_for(endpoint, **values)
