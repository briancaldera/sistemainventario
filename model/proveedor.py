from peewee import Model, AutoField, CharField, DateField
from datetime import datetime

from db.database import Database


class ProveedorAR(Model):
    id = AutoField()
    nombre = CharField()
    telefono = CharField()
    direccion = CharField()
    created_at = DateField()

    class Meta:
        table_name = 'proveedores'
        database = Database.get_connection()


class Proveedor:

    def __init__(self, id: int | None, nombre: str, telefono: str | None, direccion: str | None,
                 created_at: datetime | None):
        self.id: int | None = id
        self.nombre: str = nombre
        self.telefono: str | None = telefono
        self.direccion: str | None = direccion
        self.created_at: datetime | None = created_at
