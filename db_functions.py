import sqlite3
from csv import writer


def get_connection(database: str):
    conn = sqlite3.connect(database, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def exec(database: str, query: str, **parameters):
    try:
        with get_connection(database) as conn:
            result = conn.execute(query, parameters).fetchall()
        return result
    except sqlite3.DatabaseError as e:
        raise e


def exec_script(database: str, path_to_script: str):
    try:
        with get_connection(database) as conn:
            with open(path_to_script, 'r') as f:
                result = conn.executescript(f.read()).fetchall()
        return result
    except (FileNotFoundError, sqlite3.DatabaseError) as e:
        raise e


def insert_into_table(database: str, table: str, to_insert):
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


def get_pragma_info_of_table(database: str, table: str):
    try:
        with get_connection(database) as conn:
            pragma = conn.execute(
                f'SELECT name, type FROM pragma_table_info("{table}")'
            ).fetchall()
        return {tup[0]: tup[1] for tup in pragma}
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
