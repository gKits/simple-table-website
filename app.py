import sqlite3
from flask import Flask, render_template, request, redirect, send_file
from csv import writer


app = Flask(__name__)
INSERT = 'INSERT INTO person (Name, Firstname, Age) VALUES (?, ?, ?)'
DELETE = 'DELETE FROM person WHERE Id=?'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def db_to_csv():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM person')
    with open('./csv/output.csv', 'w', newline='') as f:
        wr = writer(f, dialect='excel')
        wr.writerow([header[0] for header in data.description])
        wr.writerows(data)
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        conn = get_db_connection()
        data = conn.execute('SELECT * FROM person')
        headings = [header[0] for header in data.description]
        conn.close

        return render_template(
            'index.html',
            headings=headings,
            data=data,
            title='Table'
        )
    elif request.method == 'POST':
        id = request.form['delete']
        conn = get_db_connection()
        conn.execute(DELETE, id)
        conn.commit()
        conn.close()

        return redirect('/')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template(
            'create.html',
            inputs=['Hello', 'World'],
            title='Table'
        )
    elif request.method == 'POST':
        if request.form['submit'] == 'add_person':
            try:
                name = request.form['name']
                firstname = request.form['firstname']
                age = request.form['age']
                conn = get_db_connection()
                conn.execute(INSERT, (name, firstname, int(age)))
                conn.commit()
                conn.close()

                return redirect('/')
            except (TypeError, KeyError, sqlite3.DatabaseError):
                return redirect('/create/')


@app.route('/dlcsv/', methods=['GET'])
def get_csv():
    db_to_csv()
    return send_file('./csv/output.csv')


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
