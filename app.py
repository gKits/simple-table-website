from sqlite3 import DatabaseError
from flask import Flask, request, redirect, render_template
from flask_classful import FlaskView, route
from database import Database
from os.path import join, split


class TableView(FlaskView):
    def __init__(self, init_argument):
        self.db = Database(init_argument['db_path'])
        self.table = init_argument['displayed_table']
        self.table_pk = self.db.get_table_pk(self.table)
        self.title = f'{self.db.name}.{self.table}'
        self.autobackup = init_argument['autobackup']
        self.backup_dir = init_argument['backup_dir']

    @route('/', methods=['GET', 'POST'])
    def index(self):
        if self.autobackup:
            for table in self.db.get_all_tables():
                path = join(*split(self.backup_dir), f'{self.db.name}-{table}.csv')
                self.db.export_table_to_csv(table, path)
        if request.method == 'GET':
            pragma_info = self.db.get_pragma_table_info(self.table, 'cid')
            data = self.db.exec(f'SELECT * FROM {self.table}')
            return render_template('index.html', headings=list(pragma_info.keys()), data=data, title=self.title)
        if request.method == 'POST':
            id = request.form['delete']
            self.db.delete_row_from_table(self.table, f'{self.table_pk}={id}')
            return redirect('/')
        else:
            return redirect('/')

    @route('/create/', methods=['GET', 'POST'])
    def create(self):
        pragma_info = self.db.get_pragma_table_info(self.table, 'type', 'dflt_value')
        if request.method == 'GET':
            return render_template(
                'create.html',
                title=self.title,
                inputs=[
                    {
                        'name': name,
                        'type': pragma_info[name]['type'],
                        'default_value': pragma_info[name]['dflt_value']
                    }
                    for name in pragma_info.keys()
                ]
            )
        if request.method == 'POST':
            if request.form['submit'] == 'add':
                try:
                    self.db.insert_row_into_table(
                        table=self.table,
                        **{
                            name: request.form[name]
                            for name in pragma_info.keys()
                            if request.form[name]
                        }
                    )
                    return redirect('/')
                except (TypeError, KeyError, ValueError, DatabaseError):
                    return redirect('/create')
        else:
            return redirect('/')

    @route('/edit/<id>/', methods=['GET', 'POST'])
    def edit(self, id):
        pragma_info = self.db.get_pragma_table_info(self.table, 'type', 'dflt_value')
        data = self.db.exec(f'SELECT * FROM {self.table} WHERE {self.table_pk}={id}')

        if request.method == 'GET':
            return render_template(
                'edit.html',
                title=self.title,
                inputs=[
                    {
                        'name': name,
                        'type': pragma_info[name]['type'],
                        'data': data[0][i]
                    }
                    for i, name in enumerate(pragma_info.keys())
                ]
            )
        elif request.method == 'POST':
            try:
                if request.form['submit'] == 'edit':
                    self.db.update_rows_in_table(
                        table=self.table,
                        condition=f'{self.table_pk}={id}',
                        **{
                            name: request.form[name]
                            for i, name in enumerate(pragma_info.keys())
                            if request.form[name] != data[0][i]
                        }
                    )
                    return redirect('/')
            except (TypeError, KeyError, DatabaseError, ValueError):
                return redirect(f'/edit/{id}')


def run(db_path: str, table: str, name: str = None, port: int = None, autobackup: bool = False, backup_dir: str = None):
    app = Flask(name)
    TableView.register(
        app,
        route_base='/',
        init_argument={
            'db_path': db_path,
            'displayed_table': table,
            'autobackup': autobackup,
            'backup_dir': backup_dir
        }
    )
    app.run(use_reloader=True, port=port)


if __name__ == '__main__':
    run('./db/database.db', 'Person')
