from peewee import *

from model.cliente import Cliente
from decimal import Decimal

from model.producto import Producto
from datetime import datetime
from db.database import Database as DB
from typing import TypedDict

ItemVenta = TypedDict('ItemVenta', {'producto': Producto, 'cantidad': int, 'precio': Decimal})


class Venta(Model):
    venta_id = AutoField()
    numero_venta = CharField()
    cliente_id = ForeignKeyField(Cliente, object_id_name='id')
    total_neto = DecimalField()
    total_pagado = DecimalField()
    fecha = DateField()

    class Meta:
        table_name = "ventas"
        database = DB.get_connection()

    @staticmethod
    def crear(numero_venta: str, cliente: Cliente, total_neto: Decimal, total_pagado: Decimal,
              productos: list[ItemVenta]):
        # Start transaction here
        conn = DB.get_connection()
        with conn.atomic() as trans:
            venta = Venta.create(numero_venta=numero_venta, cliente_id=cliente.id, total_neto=total_neto,
                                 total_pagado=total_pagado, fecha=datetime.now())

            egresos = []

            for item in productos:
                egreso = Egreso.crear(venta, item['producto'], item['cantidad'], item['precio'])
                egresos.append(egreso)

            return venta, egresos


class Egreso(Model):
    egreso_id = AutoField()
    venta_id = ForeignKeyField(Venta,)
    producto_id = ForeignKeyField(Producto,)
    cantidad = IntegerField()
    precio = DecimalField()

    class Meta:
        table_name = "egresos"
        database = DB.get_connection()

    @staticmethod
    def crear(venta: Venta, producto: Producto, cantidad: int, precio: Decimal):
        conn = DB.get_connection()
        with conn.atomic() as trans:
            return Egreso.create(venta_id=venta.venta_id, producto_id=producto, cantidad=cantidad,
                                 precio=precio)
