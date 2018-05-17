#encoding=utf-8
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from  . import login_manager
from flask_login import UserMixin,AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request
from datetime import datetime
from markdown import markdown
import hashlib
#角色
class Role(db.Model):
    __tablename__='roles'

    id=db.Column(db.Integer,primary_key=True)
    #建立索引
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    name=db.Column(db.String(64),unique=True)
    #建立外键
    users = db.relationship('User', backref='role',lazy='dynamic')
    def __repr__(self):
        return '<Role %r>'%self.name

    @staticmethod
    def insert_roles():
        roles={
            'User':(Permisson.FOLLOW|
            Permisson.COMMIT|Permisson.WRITE_ARTICLES,True),
            'Administrator':(0xff,False),
            'Moderator':(Permisson.FOLLOW|Permisson.COMMIT|Permisson.WRITE_ARTICLES
                         |Permisson.MODERATE_COMMENTS,False)
        }
        #如果role角色不存在，才创建
        for r in roles:
            # print(r)
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
                role.permissions=roles[r][0]
                role.default=roles[r][1]
                db.session.add(role)
                db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Follow(db.Model):
    __tablename__='follows'

    follower_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)



#用户
class User(UserMixin, db.Model):
    __tablename__='users'

    #头像的散列值
    avatar_hash=db.Column(db.String(32))

    posts=db.relationship('Post',backref='author',lazy='dynamic')

    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)

    comments=db.relationship('Comment',backref='author',lazy='dynamic')

    name=db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 最后访问日期
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed=db.relationship('Follow',foreign_keys=[Follow.followed_id],
                             backref=db.backref('follower',lazy='joined'),
                             lazy='dynamic',cascade='all,delete-orphan')

    follower=db.relationship('Follow',foreign_keys=[Follow.follower_id],
                             backref=db.backref('followed',lazy='joined'),
                             lazy='dynamic',cascade='all,delete-orphan')

    def follow(self,user):
        if not self.is_following(user):
            f=Follow(follower=self,followed=user)
            db.session.add(f)

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()




    def unfollow(self,user):
        f=self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

        #找出当前用户关注的所有文章
    @property
    def followed_posts(self):
        return Post.query.join(Follow,Follow.followed_id==Post.author_id).\
        filter(Follow.follower_id == self.id)

#查看是否关注user用户
    def is_following(self,user):
        print(user.id)

        return self.followed.filter_by(follower_id=user.id).first() is not None

    #是否被某个用户关注
    def is_followed_by(self,user):
        return self.follower.filter_by(follower_id=user.id).first() is not None




    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()

        if not self.role:
            if self.email==current_app.config['FLASKY_ADMIN']:
                self.role=Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()
    def can(self,permissions):
        return self.role is not None\
    and (self.role.permissions & permissions)==permissions

    def isAdministrator(self):
        return self.can(Permisson.ADMINISTER)



    # 根据id生成秘钥序列
    def gernerate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def generate_email_change_token(self,new_email,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'change_email':self.id,'new_email':new_email})

    def change_email(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('change_email')!=self.id:
            return False
        new_email=data.get('new_email')
        if new_email is None:
            return False
        #如果更改的邮箱已经存在
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email=new_email
        #更新图片
        self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u=User(email=forgery_py.internet.email_address(),
                   username=forgery_py.internet.user_name(True),
                   password=forgery_py.lorem_ipsum.word(),
                   confirmed=True,
                   name=forgery_py.name.full_name(),
                   location=forgery_py.address.city(),
                   about_me=forgery_py.lorem_ipsum.sentence(),
                   member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
                print('生成成功!%d'%i)
            except IntegrityError:
                db.session.rollback()




    # 邮件认证  如果token中的confrim和self.id是一样的，说明邮件认证成功
    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False

        if data.get('confirm')!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)

        return True

    def gravatar(self,size=100,default='identicon',rating='g'):
        if request.is_secure:
            url='https://secure.gravatar.com/avatar'
        else:
            url='http://www.gravatar.com/avatar'
        hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'\
            .format(url=url,hash=hash,size=size,default=default,rating
                    =rating)

    #刷新访问时间
    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

        #check password
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>'%self.username
class Permisson:
    FOLLOW=0x01
    COMMIT=0X02
    WRITE_ARTICLES=0X04
    MODERATE_COMMENTS=0X08
    ADMINISTER=0X80

#匿名用户
class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def isAdministrator(self):
        return False
login_manager.anonymous_user=AnonymousUser


class Post(db.Model):


    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)

    body_html=db.Column(db.Text)

    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=100):
        import forgery_py
        from random import seed,randint

        seed()

        user_count=User.query.count()

        for i in range(count):
#随机挑选用户,随机生成文章
            u=User.query.offset(randint(0,user_count-1)).first()
            p=Post(body=forgery_py.lorem_ipsum.sentences(randint(1,3))
                   ,timestamp=forgery_py.date.date(True),author=u)
            db.session.add(p)

            db.session.commit()
            print('生成成功!%d' % i)

    #在储存文本时将其转换为markdown
    @ staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        import bleach
        allowed_tags=['a','abbr','acronym','b','blockquote',
                      'code','em','i','li','ol','pre','strong','ul',
                      'h1','h2','h3','p']

        target.body_html=bleach.linkify(bleach.clean(markdown(value,output_formate='html'),
                                                     tags=allowed_tags,strip=True))


db.event.listen(Post.body,'set',Post.on_changed_body)



class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)
    body_html=db.Column(db.Text)
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    disabled=db.Column(db.Boolean)
    #和post主键形成外键映射
    author_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        import bleach
        allowed_tags=['a','abbr','acronym','b','code','em',
                      'i','strong']
        target.body_html=bleach.linkify(bleach.clean(markdown(value,output_format='html'),
                    tags=allowed_tags,strip=True ))
db.event.listen(Comment.body,'set',Comment.on_changed_body)





