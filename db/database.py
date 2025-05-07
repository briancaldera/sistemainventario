import datetime

from peewee import SqliteDatabase as PeeweeSqlite, Database as PeeweeDatabase
import os
import shutil

use_in_memory = False


class Database:
    _database_filename = 'database.db'
    _instance: PeeweeDatabase | None = None

    @staticmethod
    def get_connection() -> PeeweeDatabase:
        if Database._instance is None:
            Database._instance = PeeweeSqlite(':memory:' if use_in_memory else 'database.db', pragmas={'foreign_keys': 1})

        return Database._instance

    @staticmethod
    def backup() -> bool:
        try:
            db = Database._instance
            if db is None:
                raise Exception('No database instance found')

            filename = f'backup/backup-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.db'

            # crear directorio
            if not os.path.exists('backup'):
                os.makedirs('backup')

            # close database connection
            db.close()
            shutil.copy('database.db', filename)
            db.connect()

            print(f'Database backup successful. File saved at: {filename}')
            return True
        except Exception as e:
            print(f'Error during backup: {e}')
            return False
