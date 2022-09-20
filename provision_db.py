import argparse


from os import path
import db_functions as db


def provision_db(database: str, schema: str, table: str, csv_path: str = ''):
    if path.isfile(database):
        return
    db.exec_script(database, f'./sql_schematics/{schema}')
    if csv_path is not None and path.isfile(csv_path):
        db.insert_csv_into_table(database, table, csv_path)


def main():
    parser = argparse.ArgumentParser(
        'Provision SQLite database',
        description='Options for the DB proviosioning for your table website'
    )

    parser.add_argument(
        '-d', '--database'
    )
    parser.add_argument(
        '-c', '-csv'
    )
    parser.add_argument(
        '-s', '-sql'
    )


if __name__ == '__main__':
    main()
