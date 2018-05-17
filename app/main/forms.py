#encoding=utf-8
from wtforms import StringField,SubmitField,BooleanField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,Regexp,ValidationError
from flask_wtf import FlaskForm
from ..models import Role,User
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name = StringField('what is you name', validators=[DataRequired()])
    submit = SubmitField('submit')

class UserEditForm(FlaskForm):
    name=StringField('name',validators=[Length(0,64)])
    location=StringField('location',validators=[Length(0,64)])
    about_me=TextAreaField('about me')
    submit=SubmitField('submit')


class EditProfileAdminForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    username=StringField('Username',validators=[DataRequired(),Length(1,64),
                                                Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                       0,'Username musht have one latters'
                                                         'numbers,dots,or underscores')])
    confrimed=BooleanField('Confirmed')
    role=SelectField('Role',coerce=int)
    name=StringField('Real name',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('about me')
    submit=SubmitField('Submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        #列表推导
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

        #如果存在就不能改
    def validate_email(self,field):
        if field.data!=self.user.email and\
        User.query.filter_by(email=field.data).first():
            raise ValidationError('email already registered')

    def validate_on_submit(self,field):
        if field.data!=self.user.name and\
            User.query.filter_by(username=field.data).first():
            raise ValidationError('username already register')



class PostForm(FlaskForm):
    body=PageDownField("what's your mind",validators=[DataRequired()])
    submit=SubmitField('submit')

class CommentForm(FlaskForm):
    body=StringField('',validators=[DataRequired()])
    submit=SubmitField('Submit')

