import sqlite3


class SqliteConnection:
    db_name = "database.db"

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        return sqlite3.connect(SqliteConnection.db_name)
