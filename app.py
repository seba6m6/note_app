from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Mysuperdupersecretkey'

def connect_to_db():
    sql = sqlite3.connect(r'C:\Users\Administrator\Desktop\Coding\note_app\note_app.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_to_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['note-text']

        db = get_db()
        db.execute('insert into notes (note) values (?)', [name])
        db.commit()
        return redirect(url_for('notes'))

    return render_template('index.html')

@app.route('/notes', methods=['GET'])
def notes():
    db = get_db()
    cur = db.execute('select note from notes')
    results = cur.fetchall()

    return render_template('notes_list.html', results=results)


if __name__ == "__main__":
    app.run()