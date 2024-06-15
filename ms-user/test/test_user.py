import unittest
from flask import current_app
from app import create_app, db
from app.models.user import User
from app.services.user import UserService

service = UserService()

class UserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_user(self):
        user = User()  
        user.email = "test@example.com" 
        self.assertEqual(user.email, "test@example.com")

    def test_create_user(self):
        user = self.__createuser()
        self.assertGreaterEqual(user.id, 1)

    def __createuser(self):
        user = User()
        user.email="test@example.com"
        user.name="Emiliano"
        user.surname="Muñoz"
        user.password="1234"
        service.create(user)
        return user

    def test_find_by_id(self):
        _ = self.__createuser()
        user = service.find_by_id(1)
        self.assertIsNotNone(user) 
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.name, "Emiliano")
        self.assertEqual(user.surname, "Muñoz")
        
    def test_find_all(self):
        _ = self.__createuser()
        users = service.find_all()
        self.assertGreaterEqual(len(users), 1)

    def test_update(self):
        user=self.__createuser()
        user.email = "prueba@prueba.com"
        user.name = "Pepe"
        user.surname = "Sanchez"
        user.password = "0000"
        service.update(user, 1)
        result = service.find_by_id(1)
        self.assertEqual(result.name, user.name)
        self.assertEqual(result.surname, user.surname)
        self.assertEqual(result.email, user.email)
        self.assertEqual(result.password, user.password)

    def test_delete(self):
        _ = self.__createuser()
        service.delete(1)
        users = service.find_all()
        self.assertEqual(len(users), 0)