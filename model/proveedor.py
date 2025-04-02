from datetime import datetime

class Proveedor:
    def __init__(self, id: int | None, nombre: str, telefono: str | None, direccion: str| None, created_at: datetime | None):
        self.id: int | None = id
        self.nombre: str = nombre
        self.telefono: str | None = telefono
        self.direccion: str | None = direccion
        self.created_at: datetime| None = created_at