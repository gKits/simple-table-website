from database import Database
from os import remove
from os.path import isfile


def provision_db(db_path: str = '', sql_path: str = '', insert_tables: list = [], reprovision: bool = False):
    if isfile(db_path) and reprovision:
        remove(db_path)

    db = Database(db_path)

    if sql_path:
        db.exec_script(sql_path)

    if insert_tables:
        for tablename, csv in insert_tables:
            db.insert_from_csv_into_table(tablename, csv)
