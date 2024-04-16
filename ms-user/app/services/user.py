from app.models import User
from app.repositories import UserRepository

class UserService:
    def __init__(self):
        self.__repo = UserRepository()

    def create(self, user: User) -> User:
        return self.__repo.create(user)

    def update(self, user: User, user_id: int) -> User:
        return self.__repo.update(user, user_id)

    def delete(self, user_id: int) -> User:
        return self.__repo.delete(user_id)

    def find_all(self) -> list:
        return self.__repo.find_all()

    def find_by_id(self, user_id: int) -> User:
        return self.__repo.find_by_id(user_id)

    def find_by_email(self, email: str) -> User:
        return self.__repo.find_by_email(email)