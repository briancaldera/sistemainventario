import datetime
from argparse import ArgumentError

from model.cliente import Cliente, ClienteAR
from repository.ClienteRepository import ClienteRepository
from datetime import datetime


class ClienteService:
    def __init__(self, cliente_repository=ClienteRepository()):
        self._cliente_repository = cliente_repository
        self._cliente_repository.create_table()

    def get_all_clientes(self) -> list[Cliente]:
        return self._cliente_repository.find_all()

    def save(self, cedula: str, nombre: str, telefono: str, direccion: str) -> None:

        cedula_existe = self._chequear_cedula_existe(cedula)

        if cedula_existe:
            raise ValueError('La cédula ya se encuentra registrada')

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

    def _chequear_cedula_existe(self, cedula: str) -> bool:
        return ClienteAR.select().where(ClienteAR.cedula == cedula).first() is not None
