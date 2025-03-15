import sqlite3

from db.sqlite3.connection import SqliteConnection
from model.user import User
from valueobjects.id import Id
from valueobjects.name import Name
from valueobjects.password import Password
from datetime import datetime

'''
Repositorio para el modelo usuario.

El trabajo de los repositorios es solo ofrecer operaciones CRUD.
'''


class UserRepository:

    def create_table(self):
        with SqliteConnection.get_connection() as conn:
            conn.execute(
                'create table if not exists users (id integer primary key autoincrement, name varchar(255) not null unique, password text, created_at datetime)')

    def find(self, name: Name) -> User | None:

        with SqliteConnection.get_connection() as conn:
            cursor = conn.cursor()

            res = cursor.execute('select * from users where name = ?', [name.name])

            row = res.fetchone()

            print(row)
            if row is None:
                return None

            id = row[0]
            name = Name(row[1])
            password = Password.from_hash(row[2])
            dt = datetime.fromisoformat(row[3])

            user = User(id, name, password, dt)

            return user

    def save(self, user: User):

        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()
                res = cursor.execute('insert into users(name, password, created_at) values (?, ?, ?)',
                                     [
                                         user.name.name,
                                         user.password.hashed_pw,
                                         user.created_at,
                                     ])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()

    def delete(self, id: Id):

        with SqliteConnection.get_connection() as conn:

            try:
                cursor = conn.cursor()

                res = cursor.execute('delete from users where = ?', [id.id])

                conn.commit()
            except sqlite3.Error:
                conn.rollback()
