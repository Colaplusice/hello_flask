# encoding=utf-8
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    PasswordField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models.users import User


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Length(1, 64), Email()])

    password = PasswordField("password", validators=[DataRequired()])
    remeber_me = BooleanField("保持登录")
    submit = SubmitField("登录")


class RegisterForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        "username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ],
    )
    password = PasswordField(
        "password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="password must match"),
        ],
    )
    password2 = PasswordField("password_2", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("email aleady registered")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("username have already registered")


class ResetForm(FlaskForm):
    email = StringField("邮箱", validators=[DataRequired(), Length(1, 64), Email()])
    submite = SubmitField("提交")


class NewPassForm(FlaskForm):
    password_1 = PasswordField(
        "密码", validators=[DataRequired(), EqualTo("password_2", message="密码必须相同")]
    )
    password_2 = PasswordField("确认密码", validators=[DataRequired()])
    submite = SubmitField("提交")
