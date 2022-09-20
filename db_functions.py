import sqlite3
from csv import writer


def get_connection(database: str) -> sqlite3.Connection:
    '''
    This function will create a database connection and return it

    :param: database: The name of the database (.db File)
    :return: The database connection
    '''
    conn = sqlite3.connect(database, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def exec(database: str, command: str):
    '''
    This function executes a given command on the database

    :param: database: The name of the database (.db File)
    :param: command: The command to execute
    :return: Cursor result as list
    '''
    try:
        with get_connection(database) as conn:
            result = conn.execute(command).fetchall()
            conn.commit()
        return result
    except sqlite3.DatabaseError as e:
        raise e


def exec_script(database: str, path_to_script: str):
    '''
    This function executes a given script on the database

    :param: database: The name of the database (.db File)
    :param: path_to_script: The directory path to the script
    :return: Cursor result as list
    '''
    try:
        with get_connection(database) as conn:
            with open(path_to_script, 'r') as f:
                result = conn.executescript(f.read()).fetchall()
                conn.commit()
        return result
    except (FileNotFoundError, sqlite3.DatabaseError) as e:
        raise e


def exec_query(database: str, table: str, *query_rows: str, condition=''):
    '''
    This function will execute a query statement

    :param: database: The name of the database (.db File)
    :param: table: The table to query from
    :param: *query_rows: The rows to display from the query (Enter '*' for all)
    :param: condition: The WHERE condition (Empty by default)
    :return: Query result as list
    '''
    try:
        with get_connection(database) as conn:
            if condition:
                condition = f' WHERE {condition}'
            else:
                condition = ''
            result = conn.execute(
                f'SELECT {", ".join(query_rows)} FROM {table}{condition}'
            ).fetchall()
            conn.commit()
        return result
    except sqlite3.DatabaseError as e:
        raise e


def insert_into_table(database: str, table: str, **insert_kwargs):
    '''
    This function will insert a row from given keyword arguments into
    a given table

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to insert into
    :param: **insert_kwargs: The row parameter to insert
    :return:
    '''
    try:
        with get_connection(database) as conn:
            k_string = ', '.join(insert_kwargs.keys())
            v_string = ', '.join(['?' for _ in insert_kwargs.keys()])
            conn.execute(
                f'INSERT INTO {table} ({k_string}) VALUES({v_string});',
                [val for val in insert_kwargs.values()]
            )
            conn.commit()
    except (sqlite3.DatabaseError, ValueError) as e:
        raise e


def update_row(database: str, table: str, condition: str, **update_kwargs):
    '''
    This function will update rows of a given condition from the given
    keyword arguments

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to update
    :param: **update_kwargs: The row parameters to update
    :return:
    '''
    try:
        with get_connection(database) as conn:
            set_string = ', '.join(f'{key}=?' for key in update_kwargs.keys())
            conn.execute(
                f'UPDATE {table} SET {set_string} WHERE {condition}',
                [val for val in update_kwargs.values()]
            )
            conn.commit()
    except sqlite3.DatabaseError as e:
        raise e


def delete_row(database: str, table: str, condition: str):
    '''
    This function will update rowSs of a given condition

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to update
    :param: condition: The delete condition (e.g. "Id=10")
    :return:
    '''
    try:
        with get_connection(database) as conn:
            print(f'DELETE FROM {table} WHERE {condition}')
            conn.execute(f'DELETE FROM {table} WHERE {condition}')
            conn.commit()
    except sqlite3.DatabaseError as e:
        raise e


def get_row_names(database: str, table: str) -> list:
    '''
    This function will return all row names of a given table

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to get the row names from
    :return: list with all row names
    '''
    try:
        with get_connection(database) as conn:
            pragma = conn.execute(
                f'SELECT name FROM pragma_table_info("{table}")'
            ).fetchall()
            conn.commit()
        return [row[0] for row in pragma]
    except sqlite3.DatabaseError as e:
        raise e


def get_row_types(database: str, table: str) -> dict:
    '''
    This function will return the types of all rows of a given table

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to get the row types from
    :return: dict with the row names as keys and types as values
    '''
    try:
        with get_connection(database) as conn:
            pragma = conn.execute(
                f'SELECT name, type FROM pragma_table_info("{table}")'
            ).fetchall()
            conn.commit()
        return {row[0]: row[1] for row in pragma}
    except sqlite3.DatabaseError as e:
        raise e


def get_row_default_values(database: str, table: str) -> dict:
    '''
    This function will return the defaul values of all rows of a given table

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to get the default values from
    :return: dict with the row names as keys and types as values
    '''
    try:
        with get_connection(database) as conn:
            pragma = conn.execute(
                f'SELECT name, dflt_value FROM pragma_table_info("{table}")'
            ).fetchall()
            conn.commit()
        return {row[0]: row[1] for row in pragma}
    except sqlite3.DatabaseError as e:
        raise e


def get_row_not_null_status(database: str, table: str) -> dict:
    '''
    This function will return the value of the not null constraint of all row
    of a given table

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to get the default values from
    :return: dict with the row names as keys and types as values
    '''
    try:
        with get_connection(database) as conn:
            pragma = conn.execute(
                f'SELECT name, notnull FROM pragma_table_info("{table}")'
            ).fetchall()
            conn.commit()
        return {row[0]: row[1] for row in pragma}
    except sqlite3.DatabaseError as e:
        raise e


def db_table_to_csv(database: str, table: str, path: str) -> None:
    '''
    This function will create or write all rows of a given table to a csv file

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to write the csv from
    :param: The path to the csv file
    :return:
    '''
    try:
        with get_connection(database) as conn:
            data = conn.execute(f'SELECT * FROM {table}')
            with open(path, 'w', newline='') as f:
                wr = writer(f, dialect='excel')
                wr.writerow([header[0] for header in data.description])
                wr.writerows(data)
            conn.commit()
    except (FileNotFoundError, sqlite3.DatabaseError) as e:
        raise e


def type_casting(type: str, value: str) -> object:
    '''
    This function will parse a given value to the correct type given by the
    coresponding SQLite Type

    :param: type: The SQLite Type
    :param: value: The value to type cast
    :return: The casted value
    '''
    TYPE_CASTING = {
        'TEXT': str,
        'INTEGER': int,
        'REAL': float
    }
    try:
        casted_val = TYPE_CASTING.get(type)(value)
        return casted_val
    except (TypeError, KeyError) as e:
        raise e
