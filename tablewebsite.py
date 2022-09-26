import argparse
from app import run


def main_no():
    parser = argparse.ArgumentParser(
        'simple-table-website',
        description='Website arguments'
    )
    parser.add_argument(
        'database',
        type=str,
        help='The name of the database file containing the data.'
    )
    parser.add_argument(
        'table',
        type=str,
        help='The name of the table that you want to display.'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        action='store',
        nargs='?',
        default=5000,
        help='''The port you want to run the application on.
             Default value = 5000'''
    )

    args = vars(parser.parse_args())
    run(database=args['database'], table=args['table'], port=args['port'])


def main():
    parser = argparse.ArgumentParser('Table website', description='A small and interactive Flask website displaying the data of a SQLite DB')

    sub_parser = parser.add_subparsers(help='sub help')

    # Run parser
    parser_run = sub_parser.add_parser('run', help='Run your webiste')
    parser_run.add_argument('database', type=str, metavar='/path/to/database.db', help='Directory path to your .db file')
    parser_run.add_argument('table', type=str, help='Name of the table you want to display')
    parser_run.add_argument('-p', '--port', type=int, nargs='?', help='Port you want to run the website on')

    # DB parser
    parser_db = sub_parser.add_parser('database', help='Function for provisioning your SQLite DB')
    # parser_db.add_argument()
    parser_db.add_argument('-r', '--reprovision', action='store_true', help='If set the DB will be deleted and reprovisioned')

    args = vars(parser.parse_args())
    print(args)

if __name__ == '__main__':
    main()
