import sqlite3
import db_functions as db
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)


app = Flask(__name__)
DATABASE = 'database.db'
TABLE = 'Person'
INSERT = 'INSERT INTO Person (Name, Firstname, Age) VALUES (?, ?, ?)'
DELETE = 'DELETE FROM person WHERE Id=?'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        descriptions = db.get_row_names(DATABASE, TABLE)
        data = db.exec_query(DATABASE, TABLE, '*')
        app.logger.info(f'Excecuted SELECT * FROM {DATABASE}/{TABLE}')

        return render_template(
            'index.html',
            headings=descriptions,
            data=data,
            title='Table'
        )

    elif request.method == 'POST':
        id = request.form['delete']
        db.delete_by_id_from_table(
            database=DATABASE,
            table=TABLE,
            id=id
        )
        app.logger.info(f'Row with Id={id} deleted from "{DATABASE}/{TABLE}"')

        db.db_table_to_csv(
            database=DATABASE,
            table=TABLE,
            path=f"./csv/{DATABASE}_{TABLE}.csv"
        )
        app.logger.info(f'CSV table created from "{DATABASE}/{TABLE}"')

        return redirect('/')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    descriptions = db.get_row_names(DATABASE, TABLE)
    types = db.get_row_types(DATABASE, TABLE)
    default_values = db.get_row_default_values(DATABASE, TABLE)
    # not_null = db.get_row_not_null_status(DATABASE, TABLE)

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
                    name: db.type_casting(types[name], request.form[name])
                    for name in descriptions if request.form[name]
                }
                db.insert_into_table(
                    DATABASE,
                    TABLE,
                    **insert_kwargs
                )
                app.logger.info(
                    f'Inserted {insert_kwargs} into "{DATABASE}/{TABLE}"'
                )

                db.db_table_to_csv(
                    database=DATABASE,
                    table=TABLE,
                    path=f"./csv/{DATABASE}_{TABLE}.csv"
                )
                app.logger.info(f'CSV table created from "{DATABASE}/{TABLE}"')

                return redirect('/')
            except (
                TypeError,
                KeyError,
                sqlite3.DatabaseError,
                ValueError
            ) as e:
                app.logger.error(e)
                return redirect('/create/')


@app.route('/edit/<id>/', methods=['GET', 'POST'])
def edit(id):
    descriptions = db.get_row_names(DATABASE, TABLE)
    types = db.get_row_types(DATABASE, TABLE)
    data = db.exec_query(DATABASE, TABLE, '*', condition=f'Id={id}')
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
                    if request.form[name] != data[0][descriptions.index(name)]
                }
                print(changes)
                db.update_row(DATABASE, TABLE, f'Id={id}', **changes)
                return redirect('/')
        except (
                TypeError,
                KeyError,
                sqlite3.DatabaseError,
                ValueError
        ) as e:
            app.logger.error(e)
            return redirect(f'/edit/{id}')


@app.route('/dlcsv/', methods=['GET'])
def get_csv():
    return send_file('./csv/output.csv')


def main(database: str, table_to_display: str):
    pass


if __name__ == '__main__':
    # main()
    app.run(use_reloader=True, debug=True)
