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
        descriptions = db.get_pragma_info_of_table(
                    database=DATABASE,
                    table=TABLE
        ).keys()
        app.logger.info(
            f'Got row names {descriptions} of "{DATABASE}/{TABLE}"'
        )

        data = db.exec(
            database=DATABASE,
            query=f'SELECT * FROM {TABLE}'
        )
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
    pragma = db.get_pragma_info_of_table(
                    database=DATABASE,
                    table=TABLE
    )
    descriptions = pragma.keys()
    app.logger.info(f'Got Pragma table {pragma} of "{DATABASE}/{TABLE}"')

    if request.method == 'GET':
        return render_template(
            'create.html',
            inputs=descriptions,
            title='Table'
        )
    elif request.method == 'POST':
        if request.form['submit'] == 'add_person':
            try:
                to_insert = {
                        title: db.type_casting(
                            type=pragma[title],
                            value=request.form[title]
                        )
                        for title in descriptions
                        if request.form[title]
                }
                db.insert_into_table(
                    database=DATABASE,
                    table=TABLE,
                    to_insert=to_insert
                )
                app.logger.info(
                    f'Inserted {to_insert} into "{DATABASE}/{TABLE}"'
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


@app.route('/dlcsv/', methods=['GET'])
def get_csv():
    return send_file('./csv/output.csv')


def main(database: str, table_to_display: str):
    pass


if __name__ == '__main__':
    # main()
    app.run(use_reloader=True, debug=True)
