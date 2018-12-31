from app import db
from app.models.models import Permission
from app import login_manager
from app.utils import SerializeMixin


# 角色
class Role(db.Model, SerializeMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name

    @staticmethod
    def insert_roles():
        roles = {
            "User": (
                Permission.FOLLOW | Permission.COMMIT | Permission.WRITE_ARTICLES,
                True,
            ),
            "Administrator": (0xFF, False),
            "Moderator": (
                Permission.FOLLOW
                | Permission.COMMIT
                | Permission.WRITE_ARTICLES
                | Permission.MODERATE_COMMENTS,
                False,
            ),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
                db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    from .users import User

    return User.query.get(int(user_id))
