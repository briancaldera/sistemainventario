from peewee import *

from model.producto import Producto
from model.proveedor import Proveedor
from decimal import Decimal
from datetime import datetime
from typing import TypedDict

from db.database import Database as DB

ItemCompra = TypedDict('ItemCompra', {'producto': Producto, 'cantidad': int, 'precio': Decimal})


class Compra(Model):
    compra_id = AutoField()
    numero_compra = CharField()
    proveedor_id = ForeignKeyField(Proveedor, object_id_name='id')
    costo_total = DecimalField()
    fecha = DateField()

    ingresos = []

    class Meta:
        table_name = "compras"
        database = DB.get_connection()

    @staticmethod
    def crear(numero_compra: str, proveedor: Proveedor, costo_total: Decimal,
              productos: list[ItemCompra]):
        # Start transaction here
        with Compra.Meta.database.atomic() as trans:
            compra = Compra.create(numero_compra=numero_compra, proveedor_id=proveedor.id, costo_total=costo_total,
                                   fecha=datetime.now())

            ingresos = []

            for item in productos:
                ingreso = Ingreso.crear(compra, item['producto'], item['cantidad'], item['precio'])
                ingresos.append(ingreso)

            return compra, ingresos


class Ingreso(Model):
    ingreso_id = AutoField()
    compra_id = ForeignKeyField(Compra,)
    producto_id = ForeignKeyField(Producto,)
    cantidad = IntegerField()
    costo = DecimalField()

    class Meta:
        table_name = "ingresos"
        database = DB.get_connection()

    @staticmethod
    def crear(compra: Compra, producto: Producto, cantidad: int, costo: Decimal):
        with Ingreso.Meta.database.atomic() as trans:
            return Ingreso.create(compra_id=compra.compra_id, producto_id=producto.producto_id, cantidad=cantidad,
                                  costo=costo)
