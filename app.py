import db_functions as db
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)
from sqlite3 import DatabaseError
from app_wrapper_class import FlaskAppWrapper, EndpointAction


def index():
    if request.method == 'GET':
        pass


class TableEndpoints:

    def __init__(self, database: str, table: str):
        self.database = f'./db/{database}'
        self.db_name = database
        self.table = table

    def index(self):
        return 'Hello world'
        db.db_table_to_csv(
            database=self.database,
            table=self.table,
            csv_path=f"./csv/{self.db_name[:-3]}-{self.table}.csv"
        )
        if request.method == 'GET':
            descriptions = db.get_row_names(self.database, self.table)
            data = db.exec_query(self.database, self.table, '*')

            return render_template(
                'index.html',
                headings=descriptions,
                data=data,
                title='Table'
            )

        elif request.method == 'POST':
            id = request.form['delete']
            db.delete_row(self.database, self.table, f'Id={id}')

            return redirect('/')


    def create(self):
        descriptions = db.get_row_names(self.database, self.table)
        types = db.get_row_types(self.database, self.table)
        default_values = db.get_row_default_values(
            self.database,
            self.table
        )
        # not_null = db.get_row_not_null_status(self.database, self.table)

        if request.method == 'GET':
            return render_template(
                'create.html',
                inputs=[
                    {
                        'name': name,
                        'type': types[name],
                        'default_value': default_values[name],
                        # 'not_null': not_null[name]
                    }
                    for name in descriptions
                ],
                title='Table'
            )
        elif request.method == 'POST':
            if request.form['submit'] == 'add':
                try:
                    insert_kwargs = {
                        name: db.type_casting(
                            types[name],
                            request.form[name]
                        )
                        for name in descriptions if request.form[name]
                    }
                    db.insert_into_table(
                        self.database,
                        self.table,
                        **insert_kwargs
                    )

                    return redirect('/')
                except (
                    TypeError,
                    KeyError,
                    DatabaseError,
                    ValueError
                ):
                    return redirect('/create/')


    def edit(self, id):
        descriptions = db.get_row_names(self.database, self.table)
        types = db.get_row_types(self.database, self.table)
        data = db.exec_query(
            self.database,
            self.table,
            '*',
            condition=f'Id={id}'
        )
        if request.method == 'GET':
            return render_template(
                'edit.html',
                inputs=[
                    {
                        'name': name,
                        'type': types[name],
                        'data': data[0][i]
                    }
                    for i, name in enumerate(descriptions)
                ],
                title='Table'
            )
        elif request.method == 'POST':
            try:
                if request.form['submit'] == 'edit':
                    db.update_row(
                        self.database,
                        self.table,
                        f'Id={id}',
                        **{
                            name: request.form[name]
                            for i, name in enumerate(descriptions)
                            if request.form[name] != data[0][i]
                        }
                    )
                    return redirect('/')
            except (
                    TypeError,
                    KeyError,
                    DatabaseError,
                    ValueError
            ):
                return redirect(f'/edit/{id}')


def start(database: str, table: str, name: str='table_website', port: int=None):
    app = FlaskAppWrapper(name, port=port)
    tbl_enp = TableEndpoints(database, table)
    app.add_endpoint(endpoint='/', endpoint_name='index', handler=tbl_enp.index)
    app.add_endpoint(endpoint='/create', endpoint_name='create', handler=EndpointAction(tbl_enp.create))
    app.add_endpoint(endpoint='/edit', endpoint_name='edit', handler=EndpointAction(tbl_enp.edit))
    app.run()


if __name__ == '__main__':
    start('./db/database.db', 'Person')
