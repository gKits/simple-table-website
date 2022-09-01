import sqlite3
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
INSERT = 'INSERT INTO person (name, firstname, age) VALUES (?, ?, ?)'
DELETE = 'DELETE FROM person WHERE Id={}'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        conn = get_db_connection()
        data = conn.execute('SELECT * FROM person')
        headings = [header[0] for header in data.description]
        conn.close

        return render_template(
            'index.html',
            title='Table',
            headings=headings,
            data=data
        )
    elif request.method == 'POST':
        id = request.form['delete']
        conn = get_db_connection()
        conn.execute(DELETE.format(id))
        conn.commit()
        conn.close()

        return redirect('/')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
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
            except Exception:
                pass
        redirect('/create/')


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
