import datetime

from model.cliente import Cliente
from repository.ClienteRepository import ClienteRepository
from datetime import datetime


class ClienteService:
    def __init__(self, cliente_repository=ClienteRepository()):
        self._cliente_repository = cliente_repository
        self._cliente_repository.create_table()

    def get_all_clientes(self) -> list[Cliente]:
        return self._cliente_repository.find_all()

    def save(self, cedula: str, nombre: str, telefono: str, direccion: str) -> None:
        cliente = Cliente(
            id=None,
            cedula=cedula,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            created_at=datetime.now()
        )

        self._cliente_repository.save(cliente)

    def update_cliente(self, id: int, data: dict) -> None:
        cliente = self._cliente_repository.find(id)

        if cliente is None:
            raise Exception('ID no válido')

        for k, v in data.items():
            setattr(cliente, k, v)

        self._cliente_repository.update(cliente)

    def delete_cliente(self, id: int) -> None:
        self._cliente_repository.delete(id)
