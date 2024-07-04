from app.models import User
from app.repositories import UserRepository
from app import cache, db
import requests
import os
from dotenv import load_dotenv
from retrying import retry

load_dotenv()

class UserService:
    def __init__(self):
        self.__repo = UserRepository()
        self.cabin_api_url = os.getenv('CABIN_API_URL')
        self.cache_timeout = int(os.getenv('CACHE_TIMEOUT', 50))

    @retry(stop_max_attempt_number=3, wait_fixed=1000, retry_on_exception=lambda e: isinstance(e, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)))
    @cache.memoize(timeout=50)
    def find_all(self) -> list:
        try:
            users = self.__repo.find_all()
            return users if users else []
        except Exception as e:
            raise Exception("An error occurred while trying to retrieve the users") from e
    
    @retry(stop_max_attempt_number=3, wait_fixed=1000, retry_on_exception=lambda e: isinstance(e, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)))
    def get_cabins(self):
        try:
            response = requests.get(self.cabin_api_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception("An error occurred while trying to communicate with the cabin service") from e
    
    @retry(stop_max_attempt_number=3, wait_fixed=1000, retry_on_exception=lambda e: isinstance(e, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)))
    def post_user(self, user: User) -> User:
        try:
            created_user = self.__repo.create(user)
            cache.set(f"user_{created_user.id}", created_user, timeout=self.cache_timeout)
            return created_user
        except Exception as e:
            raise Exception("An error occurred while trying to create the user") from e

    def update(self, user: User, user_id: int) -> User:
        try:
            existing_user = self.__repo.find_by_id(user_id)
            if existing_user:
                existing_user.name = user.name
                existing_user.surname = user.surname
                existing_user.email = user.email
                db.session.commit()
                cache.set(f"user_{existing_user.id}", existing_user, timeout=self.cache_timeout)
                return existing_user
            return None
        except Exception as e:
            db.session.rollback()
            raise Exception("An error occurred while trying to update the user") from e

    def delete(self, user_id: int) -> User:
        try:
            result = self.__repo.delete(user_id)
            cache.delete(f"user_{user_id}")
            return result
        except Exception as e:
            raise Exception("An error occurred while trying to delete the user") from e

    @cache.memoize(timeout=50)
    def find_by_id(self, user_id: int) -> User:
        try:
            user = cache.get(f"user_{user_id}")
            if user is None:
                user = self.__repo.find_by_id(user_id)
                if user:
                    cache.set(f"user_{user_id}", user, timeout=self.cache_timeout)
            return user
        except Exception as e:
            raise Exception("An error occurred while trying to retrieve the user") from e

    @cache.memoize(timeout=50)
    def find_by_email(self, email: str) -> User:
        try:
            user = cache.get(f"user_{email}")
            if user is None:
                user = self.__repo.find_by_email(email)
                if user:
                    cache.set(f"user_{email}", user, timeout=self.cache_timeout)
            return user
        except Exception as e:
            raise Exception("An error occurred while trying to retrieve the user") from e
