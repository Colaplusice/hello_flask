from app import db
from .models import Permisson


# 角色
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    # 建立索引
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    name = db.Column(db.String(64), unique=True)
    # 建立外键
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permisson.FOLLOW |
                     Permisson.COMMIT | Permisson.WRITE_ARTICLES, True),
            'Administrator': (0xff, False),
            'Moderator': (
            Permisson.FOLLOW | Permisson.COMMIT | Permisson.WRITE_ARTICLES
            | Permisson.MODERATE_COMMENTS, False)
        }
        # 如果role角色不存在，才创建
        for r in roles:
            # print(r)
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
                db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    from .Users import User
    return User.query.get(int(user_id))
