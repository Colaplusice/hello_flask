import unittest
from base64 import b64encode
from app.models.users import User, Role
from flask import url_for
from app import db, create_app
import json


class APITest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            "Authorization": "Basic"
            + b64encode((username + ":" + password).encode("utf-8")).decode("utf-8"),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    # def test_no_auth(self):
    #     response = self.client.get('/api/posts',
    #                                content_type='application/json')
    #     print('this is no auth function')
    #     print(response.status_code)
    #     self.assertTrue(response.status_code == 401)

    def test_404(self):
        response = self.client.get("/wrong_url")
        assert response.status_code == 404

    # def test_posts(self):
    #     r = Role.query.filter_by(name='User').first()
    #     self.assertIsNotNone(r)
    #
    #     u = User(
    #         email='wm@example.com',
    #         password='cat',
    #         confirmed=True,
    #         role=r)
    #
    #     db.session.add(u)
    #     db.session.commit()
    #
    #     # write an article
    #     response = self.client.post(
    #         '/api/posts/',
    #         headers=self.get_api_headers('wm@example.com', 'cat'),
    #         data=json.dumps({'body': 'body of the blog test '}))
    #     print('this is status coe')
    #     print(response.status_code)
    #     self.assertTrue(response.status_code == 201)
    #     url = response.headers.get('Location')
    #     self.assertIsNotNone(url)
    #
    #     response = self.client.get(url,
    #                                headers=self.get_api_headers('wm@163.com',
    #                                                             'cat'))
    #     self.assertTrue(response.status_code == 200)
