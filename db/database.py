from peewee import SqliteDatabase as PeeweeSqlite, Database as PeeweeDatabase


class Database:
    _instance: PeeweeDatabase | None = None

    @staticmethod
    def get_connection() -> PeeweeDatabase:
        if Database._instance is None:
            Database._instance = PeeweeSqlite('database.db')

        return Database._instance
