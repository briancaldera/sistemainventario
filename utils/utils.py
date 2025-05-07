from auth.AuthManager import AuthManager
from model.user import User


def user() -> User:
    return AuthManager.get_instance().get_user()
