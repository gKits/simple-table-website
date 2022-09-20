#! /usr/bin/env python

import argparse
from app import run


def main():
    parser = argparse.ArgumentParser(
        'simple-table-website',
        description='Website arguments'
    )
    parser.add_argument(
        '-d', '--database',
        type=str,
        action='store',
        nargs='?',
        const='database.db',
        help='''The name of the database file containing the data.
             Default value = "database.db"
             [Will be created if does not exist]'''
    )
    parser.add_argument(
        '-t', '--table',
        type=str,
        action='store',
        nargs='?',
        help='The name of the table that you want to display.'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        action='store',
        nargs='?',
        const=5000,
        help='''The port you want to run the application on.
             Default value = 5000'''
    )

    args = vars(parser.parse_args())
    run(database=args['database'], table=args['table'], port=args['port'])


if __name__ == '__main__':
    main()
