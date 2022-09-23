import argparse
import db_functions as db
from os import path, remove


def provision_db(args: dict):
    if args['reprovision'] and path.isfile(args['database']):
        remove(args['database'])

    if path.isfile(args['database']):
        return

    if path.isfile(args['sql']):
        db.exec_script(args['database'], args['sql'])

    if args['insert']:
        for table in args['insert']:
            if path.isfile(table[1]):
                db.insert_csv_into_table(args['database'], table[0], table[1])


def main():
    parser = argparse.ArgumentParser(
        'provision_db',
        description='Options for the DB proviosioning for your table website',
        allow_abbrev=False
    )

    parser.add_argument(
        '-s', '--sql',
        required=True,
        type=str,
        metavar='/path/to/sql_file.sql',
        help='Name of the sql scripts definining your table structure'
    )

    parser.add_argument(
        '-d', '--database',
        type=str,
        default='./db/database.db',
        nargs='?',
        metavar='/path/to/db_file.db',
        help='Specify database name [Default "./db/database.db"]'
    )

    parser.add_argument(
        '-i', '--insert',
        type=str,
        nargs='+',
        metavar='name_table1 /path/to/csv_table1.csv ...',
        help='Insert csv files into the corresponding tables'
    )

    parser.add_argument(
        '-r', '--reprovision',
        action='store_true',
        help='If the database already exists it will be deleted and reprovisioned'
    )

    args = vars(parser.parse_args())

    if args['insert'] is not None:
        args['insert'] = [
            (csv, args['insert'][i + 1])
            for i, csv in enumerate(args['insert']) if i % 2 == 0
        ]

    print(args)
    provision_db(args)


if __name__ == '__main__':
    main()
