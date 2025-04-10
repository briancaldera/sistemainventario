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

    def listar(self) -> list[Producto]:
        productos = Producto.select().order_by(Producto.nombre)
        return productos

    def crear(self, request: CrearProductoRequest):
        proveedor = self.proveedor_repository.find(request.proveedor_id)

        Producto.crear(request.nombre, proveedor, Decimal(request.costo), Decimal(request.precio),
                       request.existencia)

    def eliminar(self, producto_id: int):
        Producto.delete().where(Producto.producto_id == producto_id)