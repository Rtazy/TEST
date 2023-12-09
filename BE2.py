from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg
from psycopg2 import sql
from flask import jsonify
import time
from datetime import datetime

app = Flask(__name__)

# Load configuration from a separate file (config.py)
app.config.from_pyfile('config.py', silent=True)

# Connect to the database using configuration variables
conn_string = (
    f"postgresql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}@"
    f"{app.config['DB_HOST']}/{app.config['DB_NAME']}?sslmode=require"
)


#create the code in HTML for ajax:

def to_htmltable(lst):
   
   for item in lst:
     res+='<td>'

     for tem in item:
         res+="<tb>{}</tb>".format(tem)
     res+='</td>'
              
   return res

def display(querry):

   res=connect_db().cursor().execute(querry).fetchall()
   return to_htmltable(res)

#send the code to AJAX?? 

@app.route('/api/get_data')
def get_data(querry):
    # Your logic to generate or fetch updated data
    display(querry)
    updated_data = f"Updated data at {time.strftime('%H:%M:%S')}"
    return jsonify({querry: updated_data})

def connect_db():
 return pg.connect(conn_string)

def insert_data_mobin(table_name, columns, column_values):
    try:
        with connect_db() as conn, conn.cursor() as cursor:
            # Use sql.Identifier only for column names (not for table name)
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )
            cursor.execute(query, column_values)
            conn.commit()
    except pg.Error as e:
        # Handle the exception
        print(f"Error: {e}")
    
def insert_data(table_name, maxvarbin_column, other_columns, binary_data, other_column_values):
    #####
            cursor = connect_db().cursor()
    
            # Create an INSERT query with dynamic columns
            columns = [maxvarbin_column] + other_columns
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )

            # Execute the query with values
            values = [pg.Binary(binary_data)] + other_column_values
            cursor.execute(query, values)


    # Commit the transaction to persist changes
            connect_db().commit()

    # Close the cursor and connection when done
            cursor.close()
            connect_db().close()
########################################
########################################
def Select_entity(table,pkcol,entity_id):
            cursor = connect_db().cursor()
          

            query = f"SELECT * FROM {table} WHERE {pkcol} = {entity_id}"

            # Execute the query with the entity_id parameter
            cursor.execute(query)

            # Fetch the result
            entity = cursor.fetchone()

            return entity
########################################
########################################
def Select_entity(table,pkcol,entity_id):
            cursor = connect_db().cursor()
          

            query = f"SELECT * FROM {table} WHERE {pkcol} = {entity_id}"

            # Execute the query with the entity_id parameter
            cursor.execute(query)

            # Fetch the result
            entity = cursor.fetchone()

            return entity
########################################
########################################

def Del_data(table_name, primary_key_column, primary_key_value):
   
    cursor = connect_db().cursor()

    # Create an INSERT query with dynamic columns
    
    query = sql.SQL("DELETE FROM {} WHERE {}= %s").format(
        sql.Identifier(table_name), sql.Identifier(primary_key_column))


   # Execute the query with the primary key value
    cursor.execute(query, (primary_key_value,))

    # Commit the transaction to persist changes
    connect_db().commit()

    # Close the cursor and connection when done
    cursor.close()
    connect_db().close()
########################################
########################################

def Sel_data_one(table_name, primary_key_column, primary_key_value):
   
    cursor = connect_db().cursor()

    # Create an INSERT query with dynamic columns
    
    query = sql.SQL("SELECT * FROM {} WHERE {}= %s").format(
        sql.Identifier(table_name), sql.Identifier(primary_key_column))
 

   # Execute the query with the primary key value
    cursor.execute(query, (primary_key_value,))
    err=0

    ret= cursor.fetchone()
    if ret != None:
       err=1
    cursor.close()
    connect_db().close()
    return ret
########################################
########################################
def Sel_data_all(table_name, primary_key_column, primary_key_value):
   
    cursor = connect_db().cursor()

    # Create an INSERT query with dynamic columns
    
    query = sql.SQL("SELECT * FROM {} WHERE {}= %s").format(
        sql.Identifier(table_name), sql.Identifier(primary_key_column))


   # Execute the query with the primary key value
    cursor.execute(query, (primary_key_value,))

    ret= cursor.fetchall()
    cursor.close()
    connect_db().close()
    return ret
########################################
########################################
@app.route('/nouveau_beneficiere',methods=['POST','GET'])
def add_ben():
    if request.form['methods']==['POST']:
  
     Name=request.form['Name']
     gender=request.form['gender']
     Benef_social_ID=request.form['beneficiaryId']
     Disability_Category=request.form['Disability_Category']
     documents=request.files['documents']
     b_date=request.form['Birthdate']
     b_place=request.form['Birth_Place']
     Disability_sd=request.form['Disability_startdate']
     Disability_sd_con=datetime.strptime(Disability_sd,'%Y-%m-%d').date()
     bdate_conv=datetime.strptime(b_date,'%Y-%m-%d').date()
     jdate_conv=datetime.strptime(joining_date,'%Y-%m-%d').date()
     docs_bin= documents.read()
     Cols=['Full_Name','Birthdate','Birth_Place','Disability_Start_Date','Gender','Disability_Category' ]
     u=Select_entity('Beneficiary',cols,[Name,bdate_conv, b_place, gender,Disability_Category] )
     hey=""
     if u != None:
        hey="Ce membre exist deja."
     else:
         insert_data("Beneficiaries", " Documents" ,Cols, docs_bin,[Name, bdate_conv, b_place,jdate_conv,Disability_sd_con,gender,Disability_Category] )
         hey="Ce membre a ete ajoute"
   
    return render_template('Frontend/ADDBenf.html')
########################################
########################################

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
