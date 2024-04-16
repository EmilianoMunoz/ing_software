from app.models import ReserveModels as Reserve
from app.repositories import ReserveRepository

class ReserveService:
    def __init__(self):
        self.__repo = ReserveRepository()

    def create(self, reserve: Reserve) -> Reserve:
        return self.__repo.create(reserve)

    def update(self, reserve: Reserve, reserve_id: int) -> Reserve:
        return self.__repo.update(reserve, reserve_id)

    def delete(self, reserve_id: int) -> Reserve:
        return self.__repo.delete(reserve_id)

    def find_all(self) -> list:
        return self.__repo.find_all()

    def find_by_id(self, reserve_id: int) -> Reserve:
        return self.__repo.find_by_id(reserve_id)