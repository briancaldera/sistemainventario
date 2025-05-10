import datetime

from peewee import SqliteDatabase as PeeweeSqlite, Database as PeeweeDatabase
import os
import shutil

from utils.fs_util import get_resource_path

use_in_memory = False


class Database:
    _database_filename = 'database/database.db'
    _instance: PeeweeDatabase | None = None

    @staticmethod
    def get_connection() -> PeeweeDatabase:
        if Database._instance is None:
            database_filename = ':memory:' if use_in_memory else get_resource_path(Database._database_filename)

            Database._instance = PeeweeSqlite(database_filename, pragmas={'foreign_keys': 1})

        return Database._instance

    @staticmethod
    def backup() -> bool:
        try:
            db = Database._instance
            if db is None:
                raise Exception('No database instance found')

            backup_dir = get_resource_path('backup')
            filename = f'backup-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.db'

            backup_file = os.path.join(backup_dir, filename)

            # crear directorio
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            database_file = get_resource_path(Database._database_filename)

            # close database connection
            db.close()
            shutil.copy(database_file, backup_file)
            db.connect()

            print(f'Database backup successful. File saved at: {backup_file}')
            return True
        except Exception as e:
            print(f'Error during backup: {e}')
            return False
