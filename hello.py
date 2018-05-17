#encoding=utf-8
import os
from  flask import Flask,render_template,redirect,url_for,session,flash
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# __file__='/Users/cclearfanjialiang2401/Desktop/django_1/VENV_scrapy/hello_flask/sql'
base_dir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config['SECRET_KEY']='hard to gess string'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(base_dir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)

moment=Moment(app)
bootstrap=Bootstrap(app)


class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>'%self.name


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>'%self.username




def createDb():
    db.drop_all()
    db.create_all()
def createUser():
    pass
def createRole():
    admin_role=Role(name='fjl')
    admin_role.name='administrator'
    db.session.add(admin_role)
    db.session.commit()
    mod_role=Role(name='Moderator')
    user_role=Role(name='user')
    user_john=User(username='john',role=admin_role)
    user_wxp=User(username='wxp',role=user_role)

    db.session.add(admin_role)
    db.session.add(mod_role)
    db.session.add(user_role)
    db.session.add(user_john)
    db.session.add(user_wxp)

    db.session.commit()

def delete():
    mod_rol=Role.query.all()
    mod_rol=Role.query.filter_by(name='user').first()
    mod_rol=Role.query.get(name='user')
    user=User.query.filter_by

    print(mod_rol)


def makeshell_context():
    return dict(app=app,db=db,User=User,Role=Role)



if __name__ == '__main__':
    # createDb()
    # createRole()
    delete()


