
from flask import Flask, g, render_template, request
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
        return '<h1> Text：{} </h1>'.format(request.form['note-text'])
    return render_template('index.html')

if __name__ == "__main__":
    app.run()