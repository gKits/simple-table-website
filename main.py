#! /usr/bin/env python

import argparse
from email.policy import default
from app import start


def main():
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
    start(database=args['database'], table=args['table'], port=args['port'])


if __name__ == '__main__':
    main()
