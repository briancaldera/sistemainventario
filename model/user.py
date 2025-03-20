from datetime import datetime

from valueobjects.name import Name
from valueobjects.password import Password
from valueobjects.id import Id

class User:

    def __init__(self, id: Id | None, name: Name, password: Password, created_at: datetime, rol: str):
        self.id = id
        self.name = name
        self.password = password
        self.created_at = created_at
        self.rol = rol
