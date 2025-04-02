from model.proveedor import Proveedor
from repository.ProveedorRepository import ProveedorRepository
from datetime import datetime


class ProveedorService:
    def __init__(self, proveedor_repository=ProveedorRepository()):
        self._proveedor_repository = proveedor_repository
        self._proveedor_repository.create_table()

    def get_all_proveedores(self) -> list[Proveedor]:
        return self._proveedor_repository.find_all()

    def save(self, nombre: str, telefono: str, direccion: str) -> None:
        proveedor = Proveedor(
            id=None,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            created_at=datetime.now()
        )

        self._proveedor_repository.save(proveedor)

    def update_proveedor(self, id: int, data: dict) -> None:
        proveedor = self._proveedor_repository.find(id)

        if proveedor is None:
            raise Exception('ID no válido')

        for k, v in data.items():
            setattr(proveedor, k, v)

        self._proveedor_repository.update(proveedor)

    def delete_proveedor(self, id: int) -> None:
        self._proveedor_repository.delete(id)