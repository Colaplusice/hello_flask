# import unittest
# import re
# from flask import url_for
# from app import create_app, db
# from app.models.users import User
# from app.models.role import Role
#
#
# class FlaskClientTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app("testing")
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         Role.insert_roles()
#         self.client = self.app.test_client(use_cookies=True)
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()
#
#     # 测试首页
#     def test_homepage(self):
#         response = self.client.get(url_for("main.index"))
#         self.assertTrue("欢迎你" in response.get_data(as_text=True))
#
#     def test_register_and_login(self):
#         response = self.client.post(
#             url_for("auth.register"),
#             data={
#                 "email": "wm@163.com",
#                 "username": "wm",
#                 "password": "cat",
#                 "password2": "cat",
#             },
#         )
#         self.assertTrue(response.status_code == 302)
#
#         # 使用新注册的用户登录
#         response = self.client.post(
#             url_for("auth.login"),
#             data={"email": "wm@163.com", "password": "cat"},
#             follow_redirects=True,
#         )
#
#         data = response.get_data(as_text=True)
#         self.assertTrue(re.search("Hello,\swm!", data))
#         self.assertTrue("You have not confirmed your account yet." in data)
#
#         # 发送确认令牌
#
#         user = User.query.filter_by(email="wm@163.com").first()
#         token = user.generate_confirmation_token()
#         response = self.client.get(
#             url_for("auth.confirm", token=token), follow_redirects=True
#         )
#         data = response.get_data(as_text=True)
#         self.assertTrue("you have confirm your account" in data)
#
#         # 退出
#         response = self.client.get(url_for("auth.logout"), follow_redirects=True)
#         data = response.get_data(as_text=True)
#         self.assertTrue("你好~ 欢迎你" in data)
