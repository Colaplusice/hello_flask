#encoding=utf-8
from flask import render_template,redirect,request,url_for,flash
from . import auth
from .forms import LoginForm,RegisterForm
from ..models import User
from .. import db
from flask_login import current_user
from ..email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import login_required,login_user,logout_user
# @auth.route('/login')
# def login():
#     return render_template('auth/login.html')

@auth.route('/secret')
@login_required
def secret():
    return 'only authenticated user are allowed'

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        print(form)
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remeber_me.data)
            return redirect(request.args.get('next')or url_for('main.index'))
        flash('invalid username or password')

    return render_template('auth/login.html',form=form)
@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        # print('chucuole'*300)
        user=User.query.filter_by(username=form.username.data).first()
        if user is not None:
            return redirect(url_for('Register'))
            flash('have been signed')
        else:
            user=User(email=form.email.data,username=form.username.data,password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token=user.gernerate_confirmation_token()
            send_email(user.email,'Confirm your account',
                       'auth/email/confirm',user=user,token=token
                       )
            flash('A confirm email have send to your account')
            return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)

#邮件认证过来的 通过跳转过来的url 中的token 然后把token 反编码回去认证
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('you have confirm your account')
    else:
        flash('the confirm link is invalid or has expired')

    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
        if current_user.is_authenticated:
            current_user.ping()
            if not current_user.confirmed\
            and request.endpoint\
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
                return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.gernerate_confirmation_token()
    send_email(current_user.email,'Confirm your account','auth/email/confirm',
               user=current_user,token=token)
    flash('a new mail have send to your account')
    return redirect(url_for('main.index'))


