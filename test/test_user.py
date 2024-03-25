import unittest
from flask import current_app
from app import create_app
from app.models import User


class UserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_user(self):
        user = User.username = "admin"
        self.assertEqual(user.username, "admin")

    def test_user_dupled(self):
        user1 = User
        user1.username = "admin"
        user2 = User
        user2.username = "admin"
    
    def test_create_user(self):
        user = User("admin")
        user_service.create_user(user)
        self.assertEqual(user_service.get_user("admin"), user)