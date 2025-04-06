from decimal import Decimal

from peewee import *

from model.proveedor import Proveedor
from db.database import Database as DB


class Producto(Model):
    producto_id = AutoField()
    nombre = CharField()
    proveedor = ForeignKeyField(Proveedor, object_id_name='id')
    costo = DecimalField()
    precio = DecimalField()
    existencia = IntegerField()

    class Meta:
        database = DB.get_connection()

    def retirar(self, cantidad: int):
        if self.existencia < cantidad:
            raise ValueError(f'No hay suficiente en existencia: [ID] ${self.producto_id} [nombre] ${self.nombre}', self)

        self.existencia -= cantidad
        with Producto.Meta.database.atomic() as trans:
            self.save()

    def agregar(self, cantidad: int):
        self.existencia += cantidad
        with Producto.Meta.database.atomic() as trans:
            self.save()

    @staticmethod
    def crear(nombre: str, proveedor: int, costo: Decimal, precio: Decimal, existencia: int):
        with Producto.Meta.database.atomic() as trans:
            return Producto.create(nombre=nombre, proveedor=proveedor, costo=costo, precio=precio, existencia=existencia)
