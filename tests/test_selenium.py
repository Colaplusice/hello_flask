# from selenium import webdriver
# import unittest
# import threading
# from hello_flask_app import create_app
# from hello_flask_app import db
# from hello_flask_app.models import Role,User,Post
# class SeleniumTestCase(unittest.TestCase):
#     client=None
#
#     @classmethod
#     def setUpClass(cls):
#         try:
#             cls.client=webdriver.Chrome()
#         except:
#             pass
#         if cls.client:
#             cls.hello_flask_app=create_app('Testing')
#             cls.app_context=cls.hello_flask_app.app_context()
#             cls.app_context.push()
#
#         #forbid log
#         import logging
#         logger=logging.getLogger('fjl')
#         logger.setLevel('ERROR')
#
#
#         #create db
#         db.create_all()
#         Role.insert_roles()
#         User.generate_fake(10)
#         Post.generate_fake(10)
#
#
#         #add admin
#
#         admin_role=Role.query.filter_by(permisson=0xff).first()
#
#         admin=User(email='fjl2401@qq.com',username='fjl',password='cat',role=admin_role,confirm=True)
#
#         db.session.add(admin)
#
#         db.session.commit()
#
#
#         threading.Thread(target=cls.hello_flask_app.run).start()
#
#
#
#
