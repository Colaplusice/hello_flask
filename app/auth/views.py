# encoding=utf-8
from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm, RegisterForm, ResetForm, NewPassForm
from ..models.users import User
from .. import db
from flask_login import current_user
from ..celery_tasks import send_email

# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import login_required, login_user, logout_user
from ..utils import Generate_reset_password_token, verify_reset_password


# @auth.route('/login')
# def login():
#     return render_template('auth/login.html')


@auth.route("/secret")
@login_required
def secret():
    return "only authenticated user are allowed"


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            return redirect(request.args.get("next") or url_for("main.index"))
        flash("用户名或密码错误")

    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # print('chucuole'*300)
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash("注册成功")
            return redirect(url_for("Register"))
        else:
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email.delay(
                user.email,
                "Confirm your account",
                "auth/email/confirm",
                user=user,
                token=token,
            )
            flash("A confirm email have send to your account")
            return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=form)


# 忘记密码。通过邮箱重置密码
@auth.route("/reset_pass", methods=["GET", "POST"])
def reset_pass():
    form = ResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("邮箱未注册")
            return redirect(url_for("auth.login"))
        token = Generate_reset_password_token(email=email)
        send_email.delay(
            email, "重置密码", template="auth/email/reset_password", token=token
        )
        flash("一封邮件已经发送到您的账户上，请点击邮件确认")
        return redirect(url_for("main.index"))

    return render_template("auth/reset_password.html", form=form)


# 忘记密码的设置新密码
@auth.route("/change_pass/<username>", methods=["GET", "POST"])
def change_pass(username):
    form = NewPassForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        newpass = form.password_1.data
        # user
        user.set_password(newpass)
        db.session.commit()
        flash("密码修改成功!")
        return redirect(url_for("auth.login"))
    return render_template("auth/set_newpass.html", form=form)


@auth.route("/set_pass_confirm/<token>")
def set_pass_confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    # try:
    email = verify_reset_password(token)
    if email is None:
        flash("验证出现错误，链接不正确，请重新验证")
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("邮箱不存在")
        return redirect(url_for("auth.login"))
    return redirect(url_for(".change_pass", username=user.username))


# 邮件认证过来的 通过跳转过来的url 中的token 然后把token 反编码回去认证
@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        flash("you have confirm your account")
    else:
        flash("the confirm link is invalid or has expired")

    return redirect(url_for("main.index"))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if (
            not current_user.confirmed
            and request.endpoint
            and request.endpoint[:5] != "auth."
            and request.endpoint != "static"
        ):
            return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email.delay(
        current_user.email,
        "Confirm your account",
        "auth/email/confirm",
        user=current_user,
        token=token,
    )
    flash("邮件已发送到你的账户")
    return redirect(url_for("main.index"))
