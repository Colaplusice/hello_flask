import hashlib
import json
from datetime import datetime

from flask import current_app, request, url_for
from flask_login import UserMixin
from itsdangerous import BadSignature
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from .models import Post, Follow, Task, Permission, Notification
from .role import Role
from ..utils import SerializeMixin


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 发送者
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # 接受者
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Message{}>".format(self.body)


class User(UserMixin, db.Model, SerializeMixin):
    __tablename__ = "users"

    # 头像的散列值
    avatar_hash = db.Column(db.String(32))

    posts = db.relationship("Post", backref="author", lazy="dynamic")

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 最后访问日期
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # user关注的博主
    followed = db.relationship(
        "Follow",
        foreign_keys=[Follow.followed_id],
        backref=db.backref("follower", lazy="joined"),
        lazy="dynamic",
        cascade="all,delete-orphan",
    )

    # user的粉丝
    follower = db.relationship(
        "Follow",
        foreign_keys=[Follow.follower_id],
        backref=db.backref("followed", lazy="joined"),
        lazy="dynamic",
        cascade="all,delete-orphan",
    )
    tasks = db.relationship("Task", backref="user", lazy="dynamic")

    # 和message关联
    messages_sent = db.relationship(
        "Message", foreign_keys=[Message.sender_id], backref="author", lazy="dynamic"
    )
    messages_received = db.relationship(
        "Message",
        foreign_keys=[Message.recipient_id],
        backref="recipient",
        lazy="dynamic",
    )

    notifications = db.relationship("Notification", backref="user", lazy="dynamic")

    last_message_read_time = db.Column(db.DateTime)

    def new_message(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        # 返回从未看过的message
        return (
            Message.query.filter_by(recipient=self)
            .filter(Message.timestamp > last_read_time)
            .count()
        )

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def unfollow(self, user):
        f = self.followed.filter_by(follower_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()
        else:
            raise TypeError("user not found")

    # 找出当前用户关注的所有文章
    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id).filter(
            Follow.follower_id == self.id
        )

    # 查看是否关注user用户
    def is_following(self, user):

        return self.followed.filter_by(follower_id=user.id).first() is not None

    # 是否被某个用户关注
    def is_followed_by(self, user):
        return self.follower.filter_by(follower_id=user.id).first() is not None

    # 生成令牌
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id}).decode("ascii")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()

        # 配置role_id
        if not self.role:
            if self.email == current_app.config["FLASKY_ADMIN"]:
                self.role = Role.query.filter_by(permissions=0xFF).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

        # 可以在init时候再加一步，加上对自己的关注

    def can(self, permissions):
        return (
            self.role is not None
            and (self.role.permissions & permissions) == permissions
        )

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id})

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"change_email": self.id, "new_email": new_email})

    def change_email(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except ValueError:
            return False
        if data.get("change_email") != self.id:
            return False
        new_email = data.get("new_email")
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        # 更新图片
        self.avatar_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()
        db.session.add(self)
        return True

    # 自动生成信息
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(
                email=forgery_py.internet.email_address(),
                username=forgery_py.internet.user_name(True),
                password=forgery_py.lorem_ipsum.word(),
                confirmed=True,
                name=forgery_py.name.full_name(),
                location=forgery_py.address.city(),
                about_me=forgery_py.lorem_ipsum.sentence(),
                member_since=forgery_py.date.date(True),
            )
            db.session.add(u)
            try:
                db.session.commit()
                print("生成成功!%d" % i)
            except IntegrityError:
                db.session.rollback()

    # 邮件注册认证  如果token中的confrim和self.id是一样的，说明邮件认证成功
    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except BadSignature:
            return False

        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)

        return True

    # 生成图片的链接md5码
    def gravatar(self, size=100, default="identicon", rating="g"):
        if request.is_secure:
            url = "https://secure.gravatar.com/avatar"
        else:
            url = "http://www.gravatar.com/avatar"
        hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    # 刷新访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

        # check password

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)

        except BadSignature:
            return None
        return User.query.get(data["id"])

    def to_json(self):
        json_user = {
            "url": url_for("api.get_post", id=self.id, _external=True),
            "username": self.username,
            "member_since": self.member_since,
            "last_seen": self.last_seen,
            "posts": url_for("api.get_user_followed_posts", id=self.id, _external=True),
            "post_count": self.posts.count(),
        }
        return json_user

    def save_task(self, task_id):
        task = Task(id=task_id, name="user task", description="", user=self)
        db.session.add(task)

    def get_tasks_in_progress(self):
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Task.query.filter_by(user=self, name=name, complete=False).all()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        unread_messages_num = (
            Message.query.filter_by(recipient=self)
            .filter(Message.timestamp > last_read_time)
            .count()
        )
        return unread_messages_num

    def __repr__(self):
        return "<User %r>" % self.username
