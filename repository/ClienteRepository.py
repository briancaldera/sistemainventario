
import sqlite3
from datetime import datetime

from db.sqlite3.connection import SqliteConnection
from model.cliente import Cliente


class ClienteRepository:

    def create_table(self):
        with SqliteConnection.get_connection() as conn:
            conn.execute(
                'create table if not exists clientes (id integer primary key autoincrement, cedula varchar(255) not null unique, nombre varchar(255) not null, telefono varchar(255), direccion varchar(255), created_at datetime)')

    def save(self, cliente: Cliente):
        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()
                res = cursor.execute(
                    'insert into clientes(cedula, nombre, telefono, direccion, created_at) values (?, ?, ?, ?, ?)',
                    [
                        cliente.cedula,
                        cliente.nombre,
                        cliente.telefono,
                        cliente.direccion,
                        cliente.created_at,
                    ])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()

    def find(self, id: int) -> Cliente | None:
        with SqliteConnection.get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute('select * from clientes where id = ?', [id])

            row = res.fetchone()

            if row is None:
                return None

            id = row[0]
            cedula = row[1]
            nombre = row[2]
            telefono = row[3]
            direccion = row[4]
            dt = datetime.fromisoformat(row[5])

            cliente = Cliente(id, cedula, nombre, telefono, direccion, dt)

            return cliente

    def find_all(self) -> list[Cliente]:
        with SqliteConnection.get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute('select * from clientes')

            rows = res.fetchall()

            clientes = []

            for row in rows:
                id = row[0]
                cedula = row[1]
                nombre = row[2]
                telefono = row[3]
                direccion = row[4]
                dt = datetime.fromisoformat(row[5])

                cliente = Cliente(id, cedula, nombre, telefono, direccion, dt)

                clientes.append(cliente)

            return clientes

    def update(self, cliente: Cliente):
        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()

                res = cursor.execute('update clientes set cedula = ?, nombre = ?, telefono = ?, direccion = ? where id = ?',
                                     [
                                         cliente.cedula,
                                         cliente.nombre,
                                         cliente.telefono,
                                         cliente.direccion,
                                         cliente.id,
                                     ])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()

    def delete(self, id: int):

        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()

                res = cursor.execute('delete from clientes where id = ?', [id])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()