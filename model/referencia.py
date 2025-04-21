from decimal import Decimal
from peewee import *
from db.database import Database as DB
from datetime import datetime


class Referencia(Model):
    referencia_id = AutoField()
    valor = DecimalField(decimal_places=4)
    created_at = DateTimeField()

    class Meta:
        table_name = "referencias"
        database = DB.get_connection()

    def a_bolivares(self, monto: Decimal) -> Decimal:
        return monto * self.valor

    @staticmethod
    def crear(valor: Decimal):
        created_at = datetime.now()
        conn = DB.get_connection()
        with conn.atomic() as trans:
            return Referencia.create(valor=valor, created_at=created_at)
