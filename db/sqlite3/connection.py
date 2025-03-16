import sqlite3


class SqliteConnection:
    """
    Esta clase representa la conexión a la base de datos SQLite.
    Cada vez que se necesite una conexión, debería llamarse al metodo get_connection().
    De esta manera, cualquier cambio que surja, solo tendrá que hacerse acá.
    """

    db_name = "database.db"

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """
        Obtiene una conexión a la base de datos.
        :return: sqlite3.Connection
        """
        return sqlite3.connect(SqliteConnection.db_name)
