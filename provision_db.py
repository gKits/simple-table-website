from database import Database
from os import remove, listdir
from os.path import isfile, join


def provision_db(db_path: str = '', sql_dir: str = '', sql_paths: list = [], insert_tables: list = [], reprovision: bool = False):
    if isfile(db_path) and reprovision:
        remove(db_path)

    db = Database(db_path)

    if sql_paths != []:
        for sql in sql_paths:
            db.exec_script(sql)
    else:
        for filename in listdir(sql_dir):
            sql = join(sql_dir, filename)
            db.exec_script(sql)

    if insert_tables != []:
        for tablename, csv in insert_tables:
            db.insert_from_csv_into_table(tablename, csv)
