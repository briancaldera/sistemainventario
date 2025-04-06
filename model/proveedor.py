from peewee import Model
from datetime import datetime

from db.database import Database


class Proveedor(Model):
    class Meta:
        database = Database.get_connection()

    def __init__(self, id: int | None, nombre: str, telefono: str | None, direccion: str | None,
                 created_at: datetime | None):
        Model.__init__(self)
        self.id: int | None = id
        self.nombre: str = nombre
        self.telefono: str | None = telefono
        self.direccion: str | None = direccion
        self.created_at: datetime | None = created_at
