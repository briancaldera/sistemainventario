from datetime import datetime

class Cliente:
    def __init__(self, id: int | None, cedula: str, nombre: str, telefono: str | None, direccion: str| None, created_at: datetime | None):
        self.id: int | None = id
        self.cedula: str = cedula
        self.nombre: str = nombre
        self.telefono: str | None = telefono
        self.direccion: str | None = direccion
        self.created_at: datetime| None = created_at