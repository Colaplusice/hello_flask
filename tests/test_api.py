from app.models.users import Role, User
from app import db


def test_ping(client):
    res = client.get("/ping")
    assert res.status_code == 404


def test_api(client):
    Role.insert_roles()
    res = client.get("/api/roles")
    assert res.status_code == 200
    assert len(res.json) == 3


def test_no_auth(client):
    res = client.get("/api/posts")
    assert res.status_code == 401


def test_posts(client):
    Role.insert_roles()
    role = Role.query.filter_by(name="User").first()
    user = User(email="wm@example.com", password="cat", confirmed=True, role=role)
    db.session.add(user)
    db.session.commit()
    data = {"body": "body of the blog test "}
    res = client.post("/api/posts", json=data)
    print(res.status_code)
    # headers=self.get_api_headers('wm@example.com', 'cat'),
