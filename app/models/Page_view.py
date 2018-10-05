from app import db
from datetime import datetime


class View_message(db.Model):
    __tablename__ = 'view_message'
    id = db.Column(db.Integer, primary_key=True)
    # 请求url
    url = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    # 用户请求的 ip地址
    ip = db.Column(db.String(16), db.ForeignKey('user_message.user_ip')
                   )
    referrer = db.Column(db.Text, default='')
    req_method = db.Column(db.String(64), nullable=False)
    end_point = db.Column(db.String(64), nullable=False, index=True)
    user_agent = db.Column(db.String(255))

    @classmethod
    def create_from_request(cls, data):
        new_view = View_message(url=data.get('url'),
                                ip=data.get('ip'),
                                referrer=data.get('referrer'),
                                req_method=data.get('req_method'),
                                end_point=data.get('end_point'),
                                user_agent=data.get('user_agent')
                                )
        db.session.add(new_view)
        db.session.commit()


class User_message(db.Model):
    __tablename = 'user_message'
    id = db.Column(db.Integer, primary_key=True)
    user_ip = db.Column(db.String(16), nullable=False, unique=True)
    last_visit = db.Column(db.DateTime, default=datetime.now)
    views = db.relationship('View_message', backref='User_message')

    @property
    def counts(self):
        return User_message.query.count()

    @classmethod
    def create_or_update_from_request(cls, data):
        obj = User_message.query.filter_by(user_ip=data['ip']).first()
        if not obj:
            new_user_message = User_message(
                user_ip=data.get('ip')
            )
            db.session.add(new_user_message)
        else:
            obj.last_visit = datetime.now()
        db.session.commit()
