# encoding=utf-8
from wtforms import StringField, SubmitField, BooleanField, SelectField, \
    TextAreaField
import wtforms.validators
from flask_wtf import FlaskForm
from ..models import User, Role
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField(
        'what is you name',
        validators=[wtforms.validators.DataRequired()])
    submit = SubmitField('submit')


class UserEditForm(FlaskForm):
    name = StringField(
        'name',
        validators=[wtforms.validators.Length(0, 64)])
    location = StringField('location',
                           validators=[wtforms.validators.Length(0, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('submit')


# 管理员更改信息表格
class EditProfileAdminForm(FlaskForm):
    email = StringField('Email',
                        validators=[wtforms.validators.DataRequired(),
                                    wtforms.validators.Length(1, 64),
                                    wtforms.validators.Email()])
    username = StringField('Username',
                           validators=[wtforms.validators.DataRequired(),
                                       wtforms.validators.Length(1, 64),
                                       wtforms.validators.Regexp(
                                           '^[A-Za-z][A-Za-z0-9_.]*$',
                                           0,
                                           'Username musht have one latters'
                                           'numbers,dots,or underscores')])
    confrimed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name',
                       validators=[wtforms.validators.Length(0, 64)])
    location = StringField('Location',
                           validators=[wtforms.validators.Length(0, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        # 列表推导
        self.role.choices = [(role.id, role.name) for role in
                             Role.query.order_by(Role.name).all()]
        self.user = user

        # 如果存在就不能改

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise wtforms.validators.ValidationError('email already registered')

    def validate_usename(self, field):
        if field.data != self.user.name and \
                User.query.filter_by(username=field.data).first():
            raise wtforms.validators.ValidationError('用户已经注册')


class PostForm(FlaskForm):
    title = StringField('set a title for your article',
                        validators=[wtforms.validators.DataRequired()])
    body = PageDownField("what's your mind",
                         validators=[wtforms.validators.DataRequired()])
    submit = SubmitField('submit')


class CommentForm(FlaskForm):
    body = StringField('', validators=[wtforms.validators.DataRequired()])
    submit = SubmitField('Submit')


class MessageForm(FlaskForm):
    message = StringField('Message',
                          validators=[wtforms.validators.DataRequired(),
                                      wtforms.validators.Length(min=0,
                                                                max=140)])
    submit = SubmitField('提交')
