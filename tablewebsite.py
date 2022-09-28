import argparse
import sys
from app import run
from provision_db import provision_db


def parse_args():
    parser = argparse.ArgumentParser('tablewebsite', description='A small and interactive Flask website displaying the data of a SQLite DB')

    # Sub parsers
    sub_parser = parser.add_subparsers(required=True)
    parser_run = sub_parser.add_parser('run', help='Run your webiste')
    parser_db = sub_parser.add_parser('database', help='Function for provisioning your SQLite DB')

    # Run parser arguments
    parser_run.add_argument('table', type=str, help='Name of the table you want to display')
    parser_run.add_argument('-d', '--database', type=str, metavar='/path/to/database.db', default='./db/database.db', help='Path to .db file runnning your database')
    parser_run.add_argument('-n', '--name', type=str, nargs='?', default='tableapp', help='Name your websites')
    parser_run.add_argument('-p', '--port', type=int, nargs='?', default=5000, help='Specify the port you want to run the website on')

    # DB parser arguments
    group_db_sql = parser_db.add_mutually_exclusive_group()
    parser_db.add_argument('-d', '--database', type=str, metavar='/path/to/database.db', default='./db/database.db', help='Path to .db file runnning your database')
    group_db_sql.add_argument('-s', '--sql', type=str, nargs='+', metavar='/path/to/scheme.sql', help='Use specific .sql files to run on DB')
    group_db_sql.add_argument('-S', '--sqldir', type=str, nargs='?', metavar='/dir/with/sqls/database-tablename.csv', default='./sql/', help='Use a specific directory containing .sql files to run on DB')
    parser_db.add_argument('-i', '--insert', type=str, nargs='+', metavar='tablename /path/to/table.csv', help='Tuple of tablename and csv table to insert into DB')
    parser_db.add_argument('-r', '--reprovision', action='store_true', help='If set the existing DB will be deleted and reprovisioned')

    # Parse arguments
    args = vars(parser.parse_args())

    used_sub_parser = sys.argv[1]

    if used_sub_parser == 'database':
        if args['insert'] and len(args['insert']) % 2 == 0:
            args['insert'] = [(args['insert'][i], args['insert'][i + 1]) for i in range(0, len(args['insert']), 2)]
        elif args['insert'] and len(args['insert']) % 2 != 0:
            raise 'error: argument -i/--insert needs a tablename and path foreach csv file'

    return used_sub_parser, args


def main():
    used_sub_parser, args = parse_args()

    if used_sub_parser == 'database':
        provision_db(db_path=args['database'], sql_dir=args["sqldir"], sql_paths=args['sql'], insert_tables=args['insert'], reprovision=args['reprovision'])
    elif used_sub_parser == 'run':
        run(db_path=args['database'], table=args['table'], name=args['name'], port=args['port'])


if __name__ == '__main__':
    main()
