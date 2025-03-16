from datetime import datetime

from event.EventQueue import EventQueue
from model.user import User
from repository.UserRepository import UserRepository
from valueobjects.name import Name
from valueobjects.password import Password


class AuthManager:
    """
    Clase para manejar la autenticación de usuarios.
    No debe instanciarse directamente.
    Use el método get_instance() para obtener una instancia de esta clase.
    """

    _instance = None
    _user: User | None = None

    def __init__(self):
        self.userRepo = UserRepository()
        self.userRepo.create_table()

    @staticmethod
    def get_instance():
        if AuthManager._instance is None:
            AuthManager._instance = AuthManager()
        return AuthManager._instance

    def register_user(self, name: str, password) -> bool:
        """
        Registra un usuario
        :param name: nombre de usuario
        :param password: contraseña
        :return: True si el usuario se registró correctamente, False en caso contrario
        """

        # Comprobamos si el nombre de usuario ya existe
        name = Name(name)
        user = self.userRepo.find(name)

        if user is not None:
            return False

        password = Password.from_password(password)

        user = User(None, name, password, datetime.now())

        self.userRepo.save(user)

        return True

    def login(self, name, password) -> bool:
        """
        Autentica un usuario
        :param name: nombre de usuario
        :param password: contraseña
        :return:
        """

        name = Name(name)
        user = self.userRepo.find(name)

        res = user.password.compare(password)

        if res:
            self._user = user

        return res

    def logout(self) -> None:
        """
        Cierra la sesión del usuario actual
        """
        self._user = None
        EventQueue.get_instance().publish('user-logout', 'user')

    def get_user(self) -> User:
        """
        Obtiene el usuario actual
        :return: User | None
        """
        return self._user
