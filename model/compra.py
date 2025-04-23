from datetime import datetime
from decimal import Decimal
from typing import TypedDict

from peewee import *

from db.database import Database as DB
from model.producto import Producto
from model.proveedor import ProveedorAR as Proveedor
from model.referencia import Referencia

ItemCompra = TypedDict('ItemCompra', {'producto': Producto, 'cantidad': int, 'precio': Decimal})


class Compra(Model):
    compra_id = AutoField()
    numero_compra = IntegerField(unique=True)
    proveedor_id = ForeignKeyField(Proveedor, object_id_name='id')
    costo_total = DecimalField()
    referencia_id = ForeignKeyField(Referencia)
    fecha = DateField()

    ingresos = []

    class Meta:
        table_name = "compras"
        database = DB.get_connection()

    @staticmethod
    def crear(proveedor: Proveedor, costo_total: Decimal, productos: list[ItemCompra], referencia: Referencia):
        # Start transaction here

        max_compra = Compra.select(Compra.numero_compra).order_by(Compra.numero_compra.desc()).limit(1)

        numero_compra = max_compra.get().numero_compra + 1 if max_compra.exists() else 1

        conn = DB.get_connection()
        with conn.atomic() as trans:
            compra = Compra.create(numero_compra=numero_compra, proveedor_id=proveedor.id, costo_total=costo_total,
                                   fecha=datetime.now(), referencia_id=referencia.referencia_id)
            ingresos = []

            for item in productos:
                ingreso = Ingreso.crear(compra, item['producto'], item['cantidad'], item['precio'])
                ingresos.append(ingreso)

            return compra, ingresos


class Ingreso(Model):
    ingreso_id = AutoField()
    compra_id = ForeignKeyField(Compra, )
    producto_id = ForeignKeyField(Producto, )
    cantidad = IntegerField()
    costo = DecimalField()

    class Meta:
        table_name = "ingresos"
        database = DB.get_connection()

    @staticmethod
    def crear(compra: Compra, producto: Producto, cantidad: int, costo: Decimal):
        conn = DB.get_connection()
        with conn.atomic() as trans:
            return Ingreso.create(compra_id=compra, producto_id=producto, cantidad=cantidad, costo=costo)
