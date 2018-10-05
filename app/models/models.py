from app import db
from app.exceptions import ValidationError
from app import login_manager
from flask_login import AnonymousUserMixin
from flask import current_app, url_for
from datetime import datetime
from markdown import markdown
import json
import redis
import rq


class Follow(db.Model):
    __tablename__ = 'follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# 信息的传输

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 发送者
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 接受者
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message{}>'.format(self.body)


class Permisson:
    FOLLOW = 0x01
    COMMIT = 0X02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0X80
    DELETE_ARTICLE = 0X04


# 匿名用户
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def isAdministrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Post(db.Model):
    __tablename__ = 'posts'

    title = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    # comments=db.relationship('Comment',backref='author',lazy='dynamic')

    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=100):
        from .Users import User
        import forgery_py
        from random import seed, randint

        seed()

        user_count = User.query.count()

        for i in range(count):
            # 随机挑选用户,随机生成文章
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                timestamp=forgery_py.date.date(True), author=u)
            db.session.add(p)

            db.session.commit()
            print('生成成功!%d' % i)

    # add title
    @staticmethod
    def add_title():
        import forgery_py
        all_post = Post.query.all()
        for post in all_post:
            if not post.title:
                post.title = forgery_py.lorem_ipsum.title()
                db.session.add(post)
        try:
            db.session.commit()
        except Exception as e:

            print('title生成失败:%s' % e)

    # 在储存文本时将其转换为markdown
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        import bleach
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote',
                        'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']

        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_formate='html'),
                         tags=allowed_tags, strip=True))

    # 转换为json资源
    def tojson(self):
        json_post = {
            'url': url_for('api.get_post', _external=True, id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comment': url_for('api.get_comment', id=self.id, _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    # 不需要创建用户或者对象实例
    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)
    # 和post主键形成外键映射
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        import bleach
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em',
                        'i', 'strong']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True))

    def tojson(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': self.author_id,
        }
        return json_comment


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    complete = db.Column(db.Boolean, default=False)

    # 取出job
    def get_redis_queue_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except(redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=True)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

    pass


db.event.listen(Comment.body, 'set', Comment.on_changed_body)
