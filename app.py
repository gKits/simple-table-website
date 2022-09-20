import db_functions as db
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)
from sqlite3 import DatabaseError


class App:

    def __init__(self, database: str, table: str, port: int = 5000):
        self.app = Flask(__name__)
        self.database = database
        self.table = table
        self.port = port

    def start(self):
        self.app.run(use_reloader=True, debug=True, port=self.port)


app = App(database='database.db', table='Person')


@app.app.route('/', methods=['GET', 'POST'])
def index():
    db.db_table_to_csv(
        database=app.database,
        table=app.table,
        path=f"./csv/{app.database}_{app.table}.csv"
    )
    if request.method == 'GET':
        descriptions = db.get_row_names(app.database, app.table)
        data = db.exec_query(app.database, app.table, '*')

        return render_template(
            'index.html',
            headings=descriptions,
            data=data,
            title='Table'
        )

    elif request.method == 'POST':
        id = request.form['delete']
        db.delete_row(app.database, app.table, f'Id={id}')

        return redirect('/')


@app.app.route('/create/', methods=['GET', 'POST'])
def create():
    descriptions = db.get_row_names(app.database, app.table)
    types = db.get_row_types(app.database, app.table)
    default_values = db.get_row_default_values(
        app.database,
        app.table
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
                    app.database,
                    app.table,
                    **insert_kwargs
                )

                return redirect('/')
            except (
                TypeError,
                KeyError,
                DatabaseError,
                ValueError
            ) as e:
                app.app.logger.error(e)
                return redirect('/create/')


@app.app.route('/edit/<id>/', methods=['GET', 'POST'])
def edit(id):
    descriptions = db.get_row_names(app.database, app.table)
    types = db.get_row_types(app.database, app.table)
    data = db.exec_query(
        app.database,
        app.table,
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
                    'data': data[0][descriptions.index(name)]
                }
                for name in descriptions
            ],
            title='Table'
        )
    elif request.method == 'POST':
        try:
            if request.form['submit'] == 'edit':
                changes = {
                    name: request.form[name]
                    for name in descriptions
                    if request.form[name] != (
                        data[0][descriptions.index(name)]
                    )
                }
                db.update_row(
                    app.database,
                    app.table,
                    f'Id={id}',
                    **changes
                )
                return redirect('/')
        except (
                TypeError,
                KeyError,
                DatabaseError,
                ValueError
        ) as e:
            app.app.logger.error(e)
            return redirect(f'/edit/{id}')


@app.app.route('/dlcsv/', methods=['GET'])
def get_csv():
    return send_file('./csv/output.csv')


def run(database: str, table: str, port: int = 5000):
    app.database = database
    app.table = table
    app.port = port
    app.start()


if __name__ == '__main__':
    run('database.db', 'Person', 5000)
