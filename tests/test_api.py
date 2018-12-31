from app.models.users import Role


def test_api(client):
    # Role.insert_roles()
    res = client.get('/api/roles')
    assert res.status_code == 200
    print('2332')

# def get_api_headers(self, username, password):
#     return {
#         "Authorization": "Basic"
#         + b64encode((username + ":" + password).encode("utf-8")).decode("utf-8"),
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#     }

# def test_no_auth(self):
#     response = self.client.get('/api/posts',
#                                content_type='application/json')
#     print('this is no auth function')
#     print(response.status_code)
#     self.assertTrue(response.status_code == 401)

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
