from model.user import User
from repository.UserRepository import UserRepository
from valueobjects.name import Name


class UserService:
    def __init__(self, user_repository=UserRepository()):
        self._user_repository = user_repository

    def get_users(self) -> list[User]:
        return self._user_repository.find_all()

    def find_user(self, name: str) -> User:
        name = Name(name)

        return self._user_repository.find(name)

    def update_role(self, name: str, new_role: str) -> None:
        user = self.find_user(name)

        user.rol = new_role

        self._user_repository.update(user)
