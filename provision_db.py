import argparse
import db_functions as db
from os import path, remove


def provision_db(args: dict):
    if args['reprovision'] and path.isfile(args['database']):
        remove(args['database'])

    if path.isfile(args['database']):
        return

    for sql in args['sql']:
        db.exec_script(args['database'], f'./sql_schematics/{sql}')

    for table in args['csv']:
        if path.isfile(table[1]):
            db.insert_csv_into_table(args['database'], table[0], table[1])


def main():
    parser = argparse.ArgumentParser(
        'provision_db',
        description='Options for the DB proviosioning for your table website'
    )

    parser.add_argument(
        'database',
        type=str,
        metavar='[db_file_name]',
        help='The name of the database file'
    )

    parser.add_argument(
        'sql',
        type=str,
        nargs='+',
        metavar='[path_to_sql1] [path_to_sql2] ...',
        help='Paths to sql schematics with the table structure'
    )

    parser.add_argument(
        '-in', '--insert',
        type=str,
        action='append',
        metavar='[table1_name] [csv_table1] [table2_name] [csv_table2] ...',
        help='Tuples of table names and paths to csv containing data to insert'
    )

    parser.add_argument(
        '-re', '--reprovision',
        action='store_true'
    )

    args = vars(parser.parse_args())

    if args['csv'] is not None:
        args['csv'] = [
            (csv, args['csv'][i + 1])
            for i, csv in enumerate(args['csv']) if i % 2 == 0
        ]

    print(args)


if __name__ == '__main__':
    main()
