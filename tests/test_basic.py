#encoding=utf-8
import unittest
from flask import current_app
from app import create_app,db

class BasicTest(unittest.TestCase):
    #创建测试环境
    def setUp(self):
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        #测试实例是否存在
    def test_app_exist(self):
        self.assertFalse(current_app is None)

        #测试在配置环境中运行
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

