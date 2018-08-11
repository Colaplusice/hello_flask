# encoding=utf-8
import unittest
from app.models import Role
from app.models import User, Permisson, AnonymousUser
from app.models import db
from app import create_app


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')

        with self.assertRaises(AttributeError):
            u.password

    # 初始化
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    # 测试结束
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # check password is true or false
    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

        # test hash is random

    def test_password_salt_arerandom(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    # test the permission
    def test_roles_and_permissions(self):
        Role.insert_roles()

        u = User(email='mike@example.com', password='dog')
        print(u.role.permissions)
        self.assertTrue(u.can(Permisson.WRITE_ARTICLES))
        self.assertFalse(u.can(Permisson.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permisson.FOLLOW))
