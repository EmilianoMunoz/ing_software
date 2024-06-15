from app import db
from app.models import User
from app.repositories.base import Create, Read, Update, Delete
from app.mapping.user import UserSchema

class UserRepository(Create, Read, Update, Delete):

    def __init__(self):
        self.model = User

    def create(self, entity: User) -> User:
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, id: int) -> bool:
        entity = self.find_by_id(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()
            return True
        return False

    def find_by_id(self, id: int) -> User:
        return db.session.query(self.model).filter(self.model.id == id).one_or_none()

    def find_all(self) -> list:
        return db.session.query(self.model).all()

    def find_by_email(self, email: str) -> User:
        return db.session.query(self.model).filter(self.model.email == email).one_or_none()

    def update(self, user: User, id: int) -> User:
        entity = self.find_by_id(id)
        if entity:
            entity.name = user.name
            entity.surname = user.surname
            entity.email = user.email
            db.session.commit()
            return entity
        return None
