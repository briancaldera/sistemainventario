from db.database import Database
from model.compra import Compra
from model.producto import Producto
from model.proveedor import ProveedorAR
from model.referencia import Referencia
from model.venta import Venta
from repository.ClienteRepository import ClienteRepository
from repository.ProveedorRepository import ProveedorRepository
from dataclasses import dataclass
from decimal import Decimal
from typing import TypedDict

ProductoItem = TypedDict('ProductoItem', {'producto_id': int, 'cantidad': int})


class MercadeoService:
    @dataclass(frozen=True)
    class CompraRequest:
        proveedor_id: int
        costo_total: str
        lista_producto: list[ProductoItem]
        referencia_id: int

    @dataclass(frozen=True)
    class VentaRequest:
        cliente_id: int
        total_neto: str
        total_pagado: str
        lista_producto: list[ProductoItem]
        referencia_id: int

    def __init__(self):
        self.cliente_repository = ClienteRepository()
        self.proveedor_repository = ProveedorRepository()

    def listar_compras(self) -> list[Compra]:
        return Compra.select().order_by(Compra.fecha.desc())

    def listar_ventas(self) -> list[Venta]:
        return Venta.select().order_by(Venta.fecha.desc())

    def comprar(self, request: CompraRequest):

        ref = Referencia.get_by_id(request.referencia_id)

        conn = Database.get_connection()
        with conn.atomic() as trans:
            # Start transaction

            proveedor = ProveedorAR.select().where(ProveedorAR.id == request.proveedor_id).get()

            productos = []

            for item in request.lista_producto:
                producto: Producto = Producto.get_by_id(item['producto_id'])

                producto.agregar(item['cantidad'])

                productos.append({'producto': producto, 'cantidad': item['cantidad'], 'precio': producto.precio})

            Compra.crear(proveedor, Decimal(request.costo_total), productos, ref)

        # End transaction

    def vender(self, request: VentaRequest):

        ref = Referencia.get_by_id(request.referencia_id)

        conn = Database.get_connection()
        with conn.atomic() as trans:
            # Start transaction

            cliente = self.cliente_repository.find(request.cliente_id)

            productos = []

            for item in request.lista_producto:
                producto: Producto = Producto.get_by_id(item['producto_id'])

                producto.retirar(item['cantidad'])

                productos.append({'producto': producto, 'cantidad': item['cantidad'], 'precio': producto.precio})

            Venta.crear(cliente, Decimal(request.total_neto), Decimal(request.total_pagado), productos, ref)

            # End transaction
