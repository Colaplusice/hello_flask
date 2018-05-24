#encoding=utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for,abort,flash,request,current_app,make_response
from . import main
from ..models import User,Role,Comment
from ..decorators import amdin_required,permission_required
from .forms import NameForm,UserEditForm,EditProfileAdminForm,PostForm,CommentForm
from app.auth.forms import  LoginForm
from .. import db
from flask_sqlalchemy import get_debug_queries
from ..models import Permisson,Post
from flask_login import login_required,current_user

#设置cookie为0 然后跳转到Index页面
@main.route('/all')
@login_required
def show_all():
    resp=make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

#设置为1，保存用户默认习惯
@main.route('/show_followed')
@login_required
def show_followed():
    resp=make_response(redirect( url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permisson.MODERATE_COMMENTS)
def moderate():
    page=request.args.get('page',1,type=int)
    # 提取一页评论 吧把分页对象也传入html
    pagination=Comment.query.order_by(Comment.timestamp.desc())\
    .paginate(page,per_page=current_app.config['FLASKY_COMMENTS_PRE_PAGE'],
              error_out=False)

    comments=pagination.items

    return render_template('moderate.html',comments=comments,pagination=pagination,
                           page=page)

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration>=current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
                current_app.logger.warning(
                    '缓慢的语句:%s\n 参数:%s\n 持续时长:%fs\n,内容:%s\n'
                    %(query.statement,query.parameters,query.duration,query.context)
                )
    return response



@main.route('/',methods=['GET','POST'])
def index():
    #发表文章

    form=PostForm()
    if current_user.can(Permisson.WRITE_ARTICLES)and\
        form.validate_on_submit():
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed=False
    #从cookie获得默认值
    if current_user.is_authenticated:
        show_followed=bool(request.cookies.get('show_followed',''))
    if show_followed:
            print('show follow')
            query=current_user.followed_posts
    else:
            query=Post.query
    pagination=query.order_by(Post.timestamp.desc()).paginate(
                page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False
            )
    posts=pagination.items
    return render_template('index.html',form=form,posts=posts,pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts=user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user,posts=posts)

@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    post=Post.query.get_or_404(id)
    form=CommentForm()
    if form.validate_on_submit():
        comment=Comment(body=form.body.data,post=post,author=current_user._get_current_object())
        db.session.add(comment)
        flash('your comment has been published')
        return redirect(url_for('.post',id=post.id,page=-1))
    page=request.args.get('page',1,type=int)
    if page==-1:
        page=(post.comments.count()-1)/\
             current_app.config['FLASKY_COMMENTS_PRE_PAGE']+1
    pagnation=post.comments.order_by(Comment.timestamp.asc())\
        .paginate(page,per_page=current_app.config['FLASKY_COMMENTS_PRE_PAGE'],
                  error_out=False)

    comments=pagnation.items
    return render_template('post.html',posts=[post],form=form,comments=comments,pagination=pagnation)


@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post=Post.query.get_or_404(id)
    if current_user!=post.author and \
        not current_user.can(Permisson.ADMINISTER):
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.body=form.body.data
        db.session.add(post)
        flash('the post have been updated')

        return redirect(url_for('.post',id=post.id))

    form.body.data=post.body
    return render_template('edit_post.html',form=form)


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    pass
#关注user用户
@main.route('/follow/<username>')
@login_required
@permission_required(Permisson.FOLLOW)
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for('.index'))

    if current_user.is_following(user):
        flash("you have already following user")

        return redirect(url_for('.user',username=username))

    current_user.follow(user)
    flash('you are now following the user%s.'%username)
    return  redirect(url_for('.user',username=username))

#返回用户的所有关注者
@main.route('/followers/<username>')
def followers(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash("invalid user")
        return redirect(url_for('.index'))

    page=request.args.get('page',1,type=int)

    pagination=user.follower.paginate(
        page,per_page=current_app.config['FLASKY_USER_PER_PAGE'],
        error_out=False
    )

    follows=[{'user':item.follower,'timestamp':item.timestamp
              } for item in pagination.items]

    return render_template('followers.html',user=user,title='Followers of'
                           ,endpoint='.followers',pagination=pagination
                           ,follows=follows)

#username关注的用户
@main.route('/followed_by/<username>')
def followed_by(username):
    user=User.query.filter_by(username=username).first()
    if user is  None:
        flash('invalid user')
        return redirect(url_for('.index'))

    page=request.args.get('page',1,type=int)
    pagination=user.followed.paginate(page,per_page=current_app.config['FLASKY_USER_PER_PAGE'],
                                      error_out=False)

    followed=[{'user':item.followed,'timestamp':item.timestamp}
              for item in pagination.items]

    return render_template('followers.html',user=user,title="Followed by",endpoint='.followed_by',
                           pagination=pagination,follows=followed)



@login_required
@main.route('/edit-profile',methods=['GET','POST'])
def edit_profile():

    edit_form=UserEditForm()
    if edit_form.validate_on_submit():
        current_user.name=edit_form.name.data
        current_user.location=edit_form.location.data
        current_user.about_me=edit_form.about_me.data
        db.session.add(current_user)
        flash('your data has been updated')

    edit_form.about_me.data=current_user.about_me
    edit_form.location.data=current_user.location
    edit_form.name.data=current_user.name
        #处理get数据
    return render_template('edit_profile.html',form=edit_form)

@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@amdin_required
def edit_profile_admin(id):
    #通过主键得到
    user=User.query.get_or_404(id)
    form=EditProfileAdminForm(user)

    if form.validate_on_submit():
        user.email=form.email.data
        user.username=form.username.data
        user.confirmed=form.confrimed.data
        if Role.query.filter_by(name=form.role.data).first:
            user.role=Role.query.filter_by(name=form.role.data).first()
        user.name=form.name.data
        user.about_me=form.about_me.data
        user.location=form.location.data
        db.session.add(user)
        flash('个人信息更新成功')
        return  redirect(url_for('.user',username=user.username))
    form.email.data=user.email
    form.username.data=user.username
    form.name.data=user.name
    form.about_me.data=user.about_me
    form.location.data=user.location
    form.role.data=user.role
    form.confrimed.data=user.confirmed

    return render_template('edit_profile.html',form=form,user=user)

@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permisson.MODERATE_COMMENTS)
def moderate_enable(id):
    comment=Comment.query.get_or_404(id)
    if comment and comment.disabled:
        comment.disabled=False
        db.session.add(comment)
        # 将request传递过来的page参数再传给moderate方法
    return redirect(url_for('.moderate',page=request.args.get('page',type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permisson.MODERATE_COMMENTS)
def moderate_disable(id):
    comment=Comment.query.get_or_404(id)
    if comment and not comment.disabled:
        comment.disabled=True
        db.session.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page',type=int)))