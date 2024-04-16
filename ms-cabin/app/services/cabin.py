from app.models import CabinModels as Cabin
from app.repositories import CabinRepository

class CabinService:
    def __init__(self):
        self.__repo = CabinRepository()

    def create(self, cabin: Cabin) -> Cabin:
        return self.__repo.create(cabin)

    def update(self, cabin: Cabin, cabin_id: int) -> Cabin:
        return self.__repo.update(cabin, cabin_id)

    def delete(self, cabin_id: int) -> Cabin:
        return self.__repo.delete(cabin_id)

    def find_all(self) -> list:
        return self.__repo.find_all()

    def find_by_id(self, cabin_id: int) -> Cabin:
        return self.__repo.find_by_id(cabin_id)