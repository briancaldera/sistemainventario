import sqlite3
from datetime import datetime

from db.sqlite3.connection import SqliteConnection
from model.proveedor import Proveedor


class ProveedorRepository:

    def create_table(self):
        with SqliteConnection.get_connection() as conn:
            conn.execute(
                'create table if not exists proveedores (id integer primary key autoincrement, nombre varchar(255) not null, telefono varchar(255), direccion varchar(255), created_at datetime)')

    def save(self, proveedor: Proveedor):
        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()
                res = cursor.execute(
                    'insert into proveedores(nombre, telefono, direccion, created_at) values (?, ?, ?, ?)',
                    [
                        proveedor.nombre,
                        proveedor.telefono,
                        proveedor.direccion,
                        proveedor.created_at,
                    ])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()

    def find(self, id: int) -> Proveedor | None:
        with SqliteConnection.get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute('select * from proveedores where id = ?', [id])

            row = res.fetchone()

            if row is None:
                return None

            id = row[0]
            nombre = row[1]
            telefono = row[2]
            direccion = row[3]
            dt = datetime.fromisoformat(row[4])

            proveedor = Proveedor(id, nombre, telefono, direccion, dt)

            return proveedor

    def find_all(self) -> list[Proveedor]:
        with SqliteConnection.get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute('select * from proveedores')

            rows = res.fetchall()

            proveedores = []

            for row in rows:
                id = row[0]
                nombre = row[1]
                telefono = row[2]
                direccion = row[3]
                dt = datetime.fromisoformat(row[4])

                proveedor = Proveedor(id, nombre, telefono, direccion, dt)

                proveedores.append(proveedor)

            return proveedores

    def update(self, proveedor: Proveedor):
        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()

                res = cursor.execute('update proveedores set nombre = ?, telefono = ?, direccion = ? where id = ?',
                                     [
                                         proveedor.nombre,
                                         proveedor.telefono,
                                         proveedor.direccion,
                                         proveedor.id,
                                     ])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()

    def delete(self, id: int):

        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()

                res = cursor.execute('delete from proveedores where id = ?', [id])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()
