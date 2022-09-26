from sqlite3 import DatabaseError
from flask import request, redirect, render_template
from flask_classful import FlaskView, route
from database import Database


class TableView(FlaskView):
    def __init__(self, my_init_argument):
        self.db = Database(my_init_argument['db_path'])
        self.table = my_init_argument['displayed_table']
        self.table_pk = self.db.get_table_pk(self.table)
        self.title = f'{self.db.name}.{self.table}'

    @route('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'GET':
            pragma_info = self.db.get_pragma_table_info(self.table, 'cid')
            data = self.db.exec(f'SELECT * FROM {self.table}')
            return render_template(
                'index.html',
                headings=list(pragma_info.keys()),
                data=data,
                title=self.title
            )
        if request.method == 'POST':
            id = request.form['delete']
            self.db.delete_row_from_table(self.table, f'{self.table_pk}={id}')
            return redirect('/')
        else:
            return redirect('/')

    @route('/create', methods=['GET', 'POST'])
    def create(self):
        pragma_info = self.db.get_pragma_table_info(
            self.table,
            'type',
            'dflt_value'
        )
        if request.method == 'GET':
            return render_template(
                'create.html',
                inputs=[
                    {
                        'name': k,
                        'type': pragma_info['type'],
                        'default_value': pragma_info['dflt_value']
                    }
                    for k in pragma_info.keys()
                ],
                title=self.title
            )
        if request.method == 'POST':
            if request.form['submit'] == 'add':
                try:
                    self.db.insert_row_into_table(
                        self.table,
                        **{
                            name: request.form[name]
                            for name in pragma_info.keys()
                        }
                    )
                    return redirect('/')
                except (TypeError, KeyError, ValueError, DatabaseError):
                    return redirect('/create')
        else:
            return redirect('/')

    @route('/edit/<table>/<id>', methods=['GET', 'POST'])
    def edit(self, table, id):
        if request.method == 'GET':
            pass
        if request.method == 'POST':
            pass
        else:
            return redirect('/')
