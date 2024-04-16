import unittest
from flask import current_app
from app import create_app, db
from app.models.cabin import Cabin
from app.services.cabin import CabinService

service = CabinService()

class CabinTestCase(unittest.TestCase):
    
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

    def test_cabin(self):
        cabin = Cabin()  
        cabin.type = "duplex" 
        self.assertEqual(cabin.type, "duplex")

    def test_create_cabin(self):
        cabin = self.__createcabin()
        self.assertGreaterEqual(cabin.id, 1)

    def __createcabin(self):
        cabin = Cabin()
        cabin.type="duplex"
        cabin.level="estandar"
        cabin.capacity="5"
        service.create(cabin)
        return cabin

    def test_find_by_id(self):
        _ = self.__createcabin()
        cabin = service.find_by_id(1)
        self.assertIsNotNone(cabin) 
        self.assertEqual(cabin.type, "duplex")
        self.assertEqual(cabin.level, "estandar")
        self.assertEqual(cabin.capacity, "5")
        
    def test_find_all(self):
        _ = self.__createcabin()
        cabins = service.find_all()
        self.assertGreaterEqual(len(cabins), 1)

    def test_update(self):
        cabin=self.__createcabin()
        cabin.type="duplex"
        cabin.level="estandar"
        cabin.capacity="5"
        service.update(cabin, 1)
        result = service.find_by_id(1)
        self.assertEqual(result.tpye, cabin.type)
        self.assertEqual(result.level, cabin.level)
        self.assertEqual(result.capacity, cabin.capacity)

    def test_delete(self):
        _ = self.__createcabin()
        service.delete(1)
        cabins = service.find_all()
        self.assertEqual(len(cabins), 0)