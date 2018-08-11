# import unittest
# from base64 import b64encode
# from app.models import Role,User
# from flask import url_for
# from app import db,create_app
# import json
# class APITest(unittest.TestCase):
#
#     def get_api_headers(self,username,password):
#         return {
#             'Authorization':'Basic'+b64encode(
#                 (username+':'+password).encode('utf-8')
#                     .decode('uf-8'),
#             ),
#             'Accept': 'application/json',
#             'Content-Type':'application/json',
#         }
#
#     def test_no_auth(self):
#         response=self.client.get(url_for('api.get_posts'),
#                                  content_type='application/json')
#         self.assertTrue(response.status_code==401)
#
#     def setUp(self):
#         self.app = create_app('testing')
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
#     def test_posts(self):
#         r=Role.query.filter(name='User').first()
#
#         self.assertIsNone(r)
#
#         u=User(email='wm@example.com',password='cat',confirmed=True,role=r)
#
#         db.session.add(u)
#         db.session.commit()
#
#         #write an article
#         resonse=self.client.post( url_for('api.new_post'),
#                                   headers=
#                                   self.get_auth_header('wm@example.com','cat'),
#                                   data=json.dumps({'body':'body of the blog test '})
#                                   )
#
#         self.assertTrue(resonse.status_code==201)
#         url=resonse.headers.get('Location')
#         self.assertIsNotNone(url)
#
#         response=self.client.get(url,headers=self.get_auth_header('wm@163.com','cat'))
#         self.assertTrue(response.status_code==200)
#
