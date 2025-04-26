from dataclasses import dataclass

from model.producto import Producto
from decimal import Decimal

from repository.ProveedorRepository import ProveedorRepository


class ProductoService:
    @dataclass(frozen=True)
    class CrearProductoRequest:
        nombre: str
        costo: str
        precio: str
        existencia: int

    @dataclass(frozen=True)
    class ActualizarProductoRequest:
        id: int
        nombre: str
        costo: str
        precio: str
        existencia: int

    def __init__(self):
        self.proveedor_repository = ProveedorRepository()

    def listar(self) -> list[Producto]:
        productos = Producto.select().order_by(Producto.nombre)
        return productos

    def crear(self, request: CrearProductoRequest):
        Producto.crear(request.nombre, Decimal(request.costo), Decimal(request.precio), request.existencia)

    def actualizar(self, request: ActualizarProductoRequest):
        query = Producto.update(nombre=request.nombre, costo=Decimal(request.costo), precio=Decimal(request.precio), existencia=request.existencia).where(Producto.producto_id == request.id)
        query.execute()

    def eliminar(self, producto_id: int):
        Producto.delete().where(Producto.producto_id == producto_id)