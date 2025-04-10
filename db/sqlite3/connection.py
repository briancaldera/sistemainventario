import sqlite3

from db.database import Database


class SqliteConnection:
    """
    Esta clase representa la conexión a la base de datos SQLite.
    Cada vez que se necesite una conexión, debería llamarse al metodo get_connection().
    De esta manera, cualquier cambio que surja, solo tendrá que hacerse acá.
    """

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """
        Obtiene una conexión a la base de datos.
        :return: sqlite3.Connection
        """
        return Database.get_connection().connection()
