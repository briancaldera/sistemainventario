from db.database import Database
from model.compra import Compra
from model.producto import Producto
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

    @dataclass(frozen=True)
    class VentaRequest:
        cliente_id: int
        total_neto: str
        total_pagado: str
        lista_producto: list[ProductoItem]

    def __init__(self):
        self.cliente_repository = ClienteRepository()
        self.proveedor_repository = ProveedorRepository()

    def comprar(self, request: CompraRequest):
        conn = Database.get_connection()
        with conn.atomic() as trans:
            # Start transaction
            numero_compra = ''

            proveedor = self.proveedor_repository.find(request.proveedor_id)

            productos = []

            for item in request.lista_producto:
                producto: Producto = Producto.select(Producto.producto_id == item['producto_id']).get()

                producto.agregar(item['cantidad'])

                productos.append(
                    {'producto': producto, 'cantidad': item['cantidad'], 'precio': producto.precio})

            Compra.crear(numero_compra, proveedor, Decimal(request.costo_total), productos)

        # End transaction

    def vender(self, request: VentaRequest):
        conn = Database.get_connection()
        with conn.atomic() as trans:
            # Start transaction
            numero_venta = ''

            cliente = self.cliente_repository.find(request.cliente_id)

            productos = []

            for item in request.lista_producto:
                producto: Producto = Producto.select(Producto.producto_id == item['producto_id']).get()

                producto.agregar(item['cantidad'])

                productos.append(
                    {'producto': producto, 'cantidad': item['cantidad'], 'precio': producto.precio})

            Venta.crear(numero_venta, cliente, Decimal(request.total_neto), Decimal(request.total_pagado), productos)

            # End transaction
