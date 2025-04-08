from peewee import SqliteDatabase as PeeweeSqlite, Database as PeeweeDatabase

use_in_memory = True


class Database:
    _instance: PeeweeDatabase | None = None

    @staticmethod
    def get_connection() -> PeeweeDatabase:
        if Database._instance is None:
            Database._instance = PeeweeSqlite(':memory:' if use_in_memory else 'database.db', pragmas={'foreign_keys': 1})

        return Database._instance
