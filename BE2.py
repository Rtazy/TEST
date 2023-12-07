from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg
from psycopg2 import sql
from flask import jsonify
import time
from datetime import datetime

app = Flask(__name__)
app.config['DB_USER'] = 'rimetazi_AlNour'
app.config['DB_NAME'] = 'rimetazi_AlNour'
app.config['DB_HOST'] = 'sql.bsite.net'
app.config['DB_PORT'] = 5432  # Specify the port here
app.config['DB_PASSWORD'] = '1202'

def connect_db():
    return pg.connect(
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT'],
        dbname=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD']
    )

def insert_data_mobin(table_name, columns, column_values):
   cursor = connect_db().cursor()
    
            # Create an INSERT query with dynamic columns
   
   query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )

            # Execute the query with values
   cursor.execute(query, column_values)

@app.route("/Ajouter_Annonce", methods=['GET', 'POST'])
def add_announcement():
    if request.method == 'POST':
        Ann_Title = request.form['title']
        Ann_Text = request.form['text']
        insert_data_mobin('Announcement', ['title', 'text'], [Ann_Title, Ann_Text])

    return render_template("Frontend/CreateAn.html")
@app.route('/profile')
def profile():
    return 'Hello, this is a test response from the /profile route!'

if __name__ == '__main__':
    app.run(debug=True)
