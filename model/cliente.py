from datetime import datetime

from peewee import Model, AutoField, CharField

from db.database import Database


class Cliente:

    def __init__(self, id: int | None, cedula: str, nombre: str, telefono: str | None, direccion: str | None,
                 created_at: datetime | None):
        self.id: int | None = id
        self.cedula: str = cedula
        self.nombre: str = nombre
        self.telefono: str | None = telefono
        self.direccion: str | None = direccion
        self.created_at: datetime | None = created_at


class ClienteAR(Model):
    id = AutoField()
    cedula = CharField(unique=True)
    nombre = CharField()
    telefono = CharField(null=True)
    direccion = CharField(null=True)
    created_at = CharField()

    class Meta:
        table_name = 'clientes'
        database = Database.get_connection()
