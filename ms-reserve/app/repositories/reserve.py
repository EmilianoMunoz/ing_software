from app import db
from app.models import Reserve
from app.repositories.base import Create, Read, Update, Delete

class ReserveRepository(Create, Read, Update, Delete):

    def __init__(self):
        self.model = Reserve

    def create(self, entity: Reserve) -> Reserve:
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, id: int) -> Reserve:
        entity = self.find_by_id(id)
        db.session.delete(entity)
        db.session.commit()
        return entity

    def find_by_id(self, id: int) -> Reserve:
        return db.session.query(self.model).filter(self.model.id == id).one()

    def find_all(self) -> list:
        return db.session.query(self.model).all()

    def update(self, reserve: Reserve, id: int) -> Reserve:
        entity = self.find_by_id(id)
        entity.since = reserve.since
        entity.until = reserve.until
        entity.id_user = reserve.id_user
        entity.id_cabin = reserve.id_cabin
        db.session.add(entity)
        db.session.commit()
        return entity