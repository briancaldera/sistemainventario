from decimal import Decimal

from peewee import *

from model.proveedor import ProveedorAR as Proveedor
from db.database import Database as DB


class Producto(Model):
    producto_id = AutoField()
    nombre = CharField()
    proveedor = ForeignKeyField(Proveedor, object_id_name='id')
    costo = DecimalField()
    precio = DecimalField()
    existencia = IntegerField()

    class Meta:
        table_name = "inventario"
        database = DB.get_connection()

    def retirar(self, cantidad: int):
        if self.existencia < cantidad:
            raise ValueError(f'No hay suficiente en existencia: [ID] ${self.producto_id} [nombre] ${self.nombre}', self)

        Producto.update(existencia=Producto.existencia - cantidad).where(
            Producto.producto_id == self.producto_id).execute()

    def agregar(self, cantidad: int):
        Producto.update(existencia=Producto.existencia + cantidad).where(
            Producto.producto_id == self.producto_id).execute()

    @staticmethod
    def crear(nombre: str, proveedor: Proveedor, costo: Decimal, precio: Decimal, existencia: int):
        conn = DB.get_connection()
        with conn.atomic() as trans:
            return Producto.create(nombre=nombre, proveedor=proveedor.id, costo=costo, precio=precio,
                                   existencia=existencia)
