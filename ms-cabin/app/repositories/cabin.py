from app import db
from app.models import Cabin
from app.repositories.base import Create, Read, Update, Delete

class CabinRepository(Create, Read, Update, Delete):

    def __init__(self):
        self.model = Cabin

    def create(self, entity: Cabin) -> Cabin:
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, id: int) -> Cabin:
        entity = self.find_by_id(id)
        db.session.delete(entity)
        db.session.commit()
        return entity

    def find_by_id(self, id: int) -> Cabin:
        return db.session.query(self.model).filter(self.model.id == id).one()

    def find_all(self) -> list:
        return db.session.query(self.model).all()


    def update(self, cabin: Cabin, id: int) -> Cabin:
        entity = self.find_by_id(id)
        entity.level = cabin.level
        entity.capacity = cabin.capacity
        db.session.add(entity)
        db.session.commit()
        return entity
    