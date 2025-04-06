from dataclasses import dataclass

from model.producto import Producto
from decimal import Decimal

from repository.ProveedorRepository import ProveedorRepository


class ProductoService:
    @dataclass(frozen=True)
    class CrearProductoRequest:
        nombre: str
        proveedor_id: int
        costo: str
        precio: str
        existencia: int

    def __init__(self):
        self.proveedor_repository = ProveedorRepository()

    def crear(self, request: CrearProductoRequest):
        proveedor = self.proveedor_repository.find(request.proveedor_id)

        Producto.crear(request.nombre, request.proveedor_id, Decimal(request.costo), Decimal(request.precio),
                       request.existencia)
