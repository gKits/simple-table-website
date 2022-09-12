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
        return result
    except (FileNotFoundError, sqlite3.DatabaseError) as e:
        raise e


def insert_into_table(database: str, table: str, **to_insert):
    '''
    This function will perform an INSERT statement into a given table

    :param: database: The name of the database (.db File)
    :param: table: The name of the table to insert into
    :param: *parameters: Parameters to replace "?" characters in command
    :return: Cursor result as list
    '''
    try:
        with get_connection(database) as conn:
            k_string = ', '.join(to_insert.keys())
            v_string = ', '.join(['?' for _ in to_insert.keys()])
            conn.execute(
                f'INSERT INTO {table} ({k_string}) VALUES({v_string});',
                [val for val in to_insert.values()]
            )
    except (sqlite3.DatabaseError, ValueError) as e:
        raise e


def delete_by_id_from_table(database: str, table: str, id):
    try:
        with get_connection(database) as conn:
            conn.execute(f'DELETE FROM {table} WHERE Id=?', id)
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
        return {row[0]: row[1] for row in pragma}
    except sqlite3.DatabaseError as e:
        raise e


def db_table_to_csv(database: str, table: str, path: str):
    try:
        with get_connection(database) as conn:
            data = conn.execute(f'SELECT * FROM {table}')
            with open(path, 'w', newline='') as f:
                wr = writer(f, dialect='excel')
                wr.writerow([header[0] for header in data.description])
                wr.writerows(data)
    except (FileNotFoundError, sqlite3.DatabaseError) as e:
        raise e


def type_casting(type: str, value):
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
