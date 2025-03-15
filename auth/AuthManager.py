from datetime import datetime
from model.user import User
from repository.UserRepository import UserRepository
from valueobjects.name import Name
from valueobjects.password import Password


class AuthManager:

    _listeners = []

    _instance = None
    _user = None

    def __init__(self):
        self.userRepo = UserRepository()
        self.userRepo.create_table()

    @staticmethod
    def get_instance():
        if AuthManager._instance is None:
            AuthManager._instance = AuthManager()
        return AuthManager._instance

    def register_user(self, name: str, password) -> bool:

        name = Name(name)
        user = self.userRepo.find(name)

        if user is not None:
            return False

        password = Password.from_password(password)

        user = User(None, name, password, datetime.now())

        self.userRepo.save(user)

        return True



    def login(self, name, password) -> bool:

        name = Name(name)
        user = self.userRepo.find(name)

        res = user.password.compare(password)

        if res:
            self._user = user

        return res

    def logout(self):
        self._user = None

    def get_user(self) -> User:
        return self._user

