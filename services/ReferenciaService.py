from decimal import Decimal

from model.referencia import Referencia


class ReferenciaService:
    @staticmethod
    def crear_referencia(valor: str):
        Referencia.crear(Decimal(valor))

    @staticmethod
    def listar() -> list[Referencia]:
        return Referencia.select().order_by(-Referencia.created_at)

    @staticmethod
    def conseguir_ultima_referencia() -> Referencia | None:
        referencias = Referencia.select().order_by(-Referencia.created_at)

        if len(referencias) == 0:
            return None

        return referencias[0]