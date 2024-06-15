import unittest
from flask import current_app
from app import create_app, db
from app.models.reserve import Reserve
from app.services.reserve import ReserveService

service = ReserveService()

class ReserveTestCase(unittest.TestCase):
    
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

    def test_reserve(self):
        reserve = Reserve()  
        reserve.since = "20/04/2024" 
        self.assertEqual(reserve.since, "20/04/2024")

    def test_create_reserve(self):
        reserve = self.__createreserve()
        self.assertGreaterEqual(reserve.id, 1)

    def __createreserve(self):
        reserve = Reserve()
        reserve.since="20/04/2024"
        reserve.until="24/04/2024"
        reserve.id_cabin="1"
        reserve.id_user="1"
        service.create(reserve)
        return reserve

    def test_find_by_id(self):
        _ = self.__createreserve()
        reserve = service.find_by_id(1)
        self.assertIsNotNone(reserve) 
        self.assertEqual(reserve.since, "20/04/2024")
        self.assertEqual(reserve.until, "24/04/2024")
        self.assertEqual(reserve.id_cabin, "1")
        self.assertEqual(reserve.id_user, "1")
        
    def test_find_all(self):
        _ = self.__createreserve()
        reserves = service.find_all()
        self.assertGreaterEqual(len(reserves), 1)

    def test_update(self):
        reserve=self.__createreserve()
        reserve.since="20/04/2024"
        reserve.until="24/04/2024"
        reserve.id_cabin="1"
        reserve.id_user="1"
        service.update(reserve, 1)
        result = service.find_by_id(1)
        self.assertEqual(result.since, reserve.since)
        self.assertEqual(result.until, reserve.until)
        self.assertEqual(result.id_cabin, reserve.id_cabin)
        self.assertEqual(result.id_user, reserve.id_user)

    def test_delete(self):
        _ = self.__createreserve()
        service.delete(1)
        reserves = service.find_all()
        self.assertEqual(len(reserves), 0)