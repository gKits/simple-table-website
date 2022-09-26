import sqlite3 as sql
from csv import writer
from os import path
from json import dumps


class Database:

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.name = path.split(db_path)[1][:-3]

        self.conn()

    def conn(self):
        conn = sql.connect(self.db_path)
        conn.row_factory = sql.Row
        return conn

    def exec(self, exec_statement: str):
        with self.conn() as conn:
            result = conn.execute(exec_statement).fetchall()
            conn.commit()
        return result

    def exec_script(self, script_path: str):
        with self.conn() as conn, open(script_path) as f:
            result = conn.executescript(f).fetchall()
            conn.commit()
        return result

    def create_table(self, title: str, *parameters: str):
        with self.conn() as conn:
            conn.execute(f'CREATE TABLE {title}({", ".join(parameters)});')
            conn.commit()

    def insert_row_into_table(self, table: str, **kwargs):
        pragma_info = self.get_pragma_table_info(table, 'type')
        keys_str = dumps(list(kwargs.keys()))[1:-1]
        values = [self.type_casting(pragma_info[k]["type"], v) for k, v in kwargs.items()]
        vals_str = ", ".join(["?" for _ in values])
        with self.conn() as conn:
            conn.execute(f'INSERT INTO {table} ({keys_str}) VALUES ({vals_str})', values)
            conn.commit()

    def delete_row_from_table(self, table: str, condition: str):
        with self.conn() as conn:
            conn.execute(f'DELETE FROM {table} WHERE {condition}')
            conn.commit()

    def update_rows_in_table(self, table: str, condition: str, **kwargs):
        pragma_info = self.get_pragma_table_info(table, 'type')
        set_string = ', '.join(f'{key}=?' for key in kwargs.keys())
        values = [self.type_casting(pragma_info[k]["type"], v) for k, v in kwargs.items()]
        with self.conn() as conn:
            conn.execute(f'UPDATE {table} SET {set_string} WHERE {condition}', values)
            conn.commit()

    def insert_from_csv_into_table(self, table: str, csv_path: str):
        with open(csv_path, 'r') as f:
            csv_table = [line.strip().split(',') for line in f.readlines()]
        for entry in csv_table[1:]:
            kwargs = {
                name: entry[i]
                for i, name in enumerate(csv_table[0])
            }
            self.insert_row_into_table(table, **kwargs)

    def export_table_to_csv(self, table: str, csv_path: str):
        with self.conn() as conn:
            data = conn.execute(f'SELECT * FROM {table}')
            with open(csv_path, 'w', newline='') as f:
                wr = writer(f, dialect='excel')
                wr.writerow([header[0] for header in data.description])
                wr.writerows(data)
            conn.commit()

    def row_names_of_table(self, table):
        with self.conn() as conn:
            data = conn.execute(f'SELECT * FROM {table}')
            print(data.description)

    def get_table_pk(self, table):
        pragma_info = self.get_pragma_table_info(table, 'pk')
        for k, v in pragma_info.items():
            if v['pk'] == 1:
                return k

    def get_pragma_table_info(self, table: str, *args):
        with self.conn() as conn:
            pragma = conn.execute(f'SELECT name, {", ".join(args)} FROM pragma_table_info("{table}")').fetchall()
            conn.commit()
        return {
            row[0]: {arg: row[i + 1] for i, arg in enumerate(args)}
            for row in pragma
        }

    def type_casting(self, type: str, value: str):
        TYPE_CASTING = {
            'TEXT': str,
            'INTEGER': int,
            'REAL': float
        }
        casted_val = TYPE_CASTING.get(type)(value)
        return casted_val
