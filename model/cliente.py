from datetime import datetime

from peewee import Model

from db.database import Database


class Cliente(Model):
    class Meta:
        database = Database.get_connection()

    def __init__(self, id: int | None, cedula: str, nombre: str, telefono: str | None, direccion: str| None, created_at: datetime | None):
        Model.__init__(self)
        self.id: int | None = id
        self.cedula: str = cedula
        self.nombre: str = nombre
        self.telefono: str | None = telefono
        self.direccion: str | None = direccion
        self.created_at: datetime| None = created_at