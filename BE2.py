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

def to_htmltable(data):
    res = '<table border="1">'
    
    if data:
        # Calculate colspan based on the number of columns in the first row
        colspan = len(data[0])
        
        for row in data:
            res += '<tr>'
            for col in row:
                res += '<td>'
                res += str(col)
                res += '</td>'
            res += '</tr>'
    else:
        # If no data, set colspan to 1
        colspan = 1
        res += '<tr><td colspan="{}">No data available</td></tr>'.format(colspan)
    
    res += '</table>'
    print(res)




@app.route('/api/get_data')
def get_data(querry):
    updated_data = f"Updated data at {time.strftime('%H:%M:%S')}"
    # Convert querry to a tuple if it's a list
    querry_key = tuple(querry) if isinstance(querry, list) else querry
    return jsonify({querry_key: updated_data})

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
 try:
  with connect_db() as conn, conn.cursor() as cursor:
    
            # Create an INSERT query with dynamic columns
   columns = maxvarbin_columns + other_columns
   query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns)))

         # Execute the query with values
   values = [pg.Binary(binary_data) for binary_data in binary_data_list] + other_column_values
   cursor.execute(query, values)


    # Commit the transaction to persist changes
   conn.commit()

    # Close the cursor and connection when done
   cursor.close()
   conn.close()
 except pg.Error as e:
            # Handle the exception
          print(f"Error: {e}")
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
def Sel_data_all2(table_name):
   
    cursor = connect_db().cursor()

    # Create an INSERT query with dynamic columns
    
    query = sql.SQL("SELECT * FROM {} ").format(
        sql.Identifier(table_name))


   # Execute the query with the primary key value
    cursor.execute(query)

    ret= cursor.fetchall()
    cursor.close()
    connect_db().close()
    return ret
########################################
########################################
@app.route('/nouveau_beneficiere',methods=['POST','GET'])

def add_ben():
    print("Before form submission")
    hey=""
    if request.method == 'POST':
     print("Before form submission")
     Name=request.form['Name']
     Join_Date=request.form['Join_Date']
     Benef_social_ID=request.form['beneficiaryId']
     b_date=request.form['Birthdate']
     b_place=request.form['Birth_Place']
     gender=request.form['gender']
     Disability_Category=request.form['Disability_Category']
        
     documents=request.files['documents']
     pic=request.files['picture']
      
     Disability_sd=request.form['Disability_startdate']
     Jdate_con=datetime.strptime(request.form['jdate'],'%Y-%m-%d').date()
     Disability_sd_con=datetime.strptime(Disability_sd,'%Y-%m-%d').date()
     bdate_conv=datetime.strptime(b_date,'%Y-%m-%d').date()
     docs_bin= documents.read()
     Pic_bin= pic.read()
     Cols=['Join_Date','Full_Name','Birthdate','Birth_Place','Disability_Start_Date','Gender','Disability_Category' ]
     u=Select_entity('Beneficiary',['Full_Name','Birthdate','Birth_Place','Gender','Disability_Category'],[Name,bdate_conv, b_place, gender,Disability_Category] )
     
     if u != None:
        hey="Ce membre exist deja."
     else:
         insert_data('Beneficiaries', ['Documents','picture'],Cols, [docs_bin, pic_bin],[Jdate_con,Name, bdate_conv, b_place,Disability_sd_con,gender,Disability_Category] )
         hey="Ce membre a ete ajoute"
         print("afta form submission")
   
    return render_template('Frontend/ADDBenf.html',hey=hey)
########################################
########################################
# function for Adding an assosciation's contact
@app.route("/Ajouter_Sponsor",methods=['GET','POST'])
def add_Authority():
   if request.form['methods']==['POST']:
      c_name=request.form['Name']
      c_address=request.form[' Address']
      c_email=request.form['Email ']
      c_phoneN=request.form['Phone_Number']
      Join_Date = datetime.strptime(request.form['Join_Date'], "%d/%m/%Y")
      vals=[c_name,c_address,c_email,c_phoneN,Join_Date]
      u=Select_entity("Authorities","Email",c_email)
      al=""
      if u!=None:
         al="The authority already exists"
      else:
       insert_data_mobin('Authorities',['Name','Address','Email','Phone_Number','Join_Date'],vals)
       al="The authority was successfully added"
   return render_template("Frontend/add_Auth.html",hey=hey) 

########################################
########################################
@app.route("/Ajouter_Administrateur",methods=['GET','POST'])
#the original admin must be connected  to do that
def add_admin():
   hey=""
   if request.form['methods']==['POST']:
      use_name=request.form['Admin_Name']
      use_address=request.form['Address']
      use_email=request.form['Email']
      use_phoneN=request.form['use_phoneN']
      use_pw=request.form['Password']
      u=Select_entity('Admin','Email',use_email)

 
   if u != None:
         hey="L'administrateur que vous essayer d'ajouter existe deja "
   else:
         hey="L'administrateur a ete ajoute avec succes"
         insert_data_mobin('Admin',[ 'Admin_Name','Admin_PhoneNumber', 'Address','Email','Password'],[use_name,use_phoneN,use_address,use_email,use_pw])

   return render_template("add_us.html") 

########################################
########################################
@app.route("/Ajouter_Campaingne",methods=['GET','POST'])
def add_Campaingn():
    try:
        if request.method == 'POST':
            C_Title = request.form['title']
            C_Text = request.form['text']
            C_img = request.files['picture']
            C_startd = datetime.strptime(request.form['date'], "%d/%m/%Y")
            C_endd = datetime.strptime(request.form['e_date'], "%d/%m/%Y")
            C_img_conv = C_img.read()
            insert_data("Campaign", "Img", ["Title", "Text", "start_date", "End_date"],
                        C_img_conv, [C_Title, C_Text, C_startd, C_endd])
        return render_template("Frontend/CreateCam.html")
    except Exception as e:
        # Log the exception or print it for debugging
        print(f"An error occurred: {str(e)}")
        # You can customize the error message based on the exception type
        return render_template("Frontend/error.html", error_message="An unexpected error occurred.")
########################################get_data(querry)
########################################
@app.route("/delete_donor", methods=['POST', 'GET'])
def Del_Donor():
    al = ""
    if request.method == 'POST':
        donor_id = request.form['DonorId']
        res = Select_entity("Donors", "Donors_ID", donor_id)
        
        if res is None:
            al = "Le donneur que vous avez recherche n'existe pas"
        else:
            al = "Le donneur a ete retire avec succes"
            Del_data("Donors", "Donors_ID", donor_id)

    return render_template("del_don.html", al=al)
################################################
########################################


########################################
################################################


@app.route('/Retirer_Annonce', methods=['GET', 'POST'])
def Del_Ann():
    hey = ""
    
    if request.method == 'POST':
        # Assuming you have a function like `get_data` defined somewhere
        print(Sel_data_all2("Announcement"))
        print(to_htmltable(Sel_data_all2("Announcement")))
        get_data(to_htmltable(Sel_data_all2("Announcement")))

        # Get the value of the 'announcementId' field from the form
        id = request.form['announcementId']

        # Check if the announcement with the provided ID exists
        res = Select_entity("Announcement", "Announcement_ID", id)

        if res is None:
            hey = "L'annonce que vous avez recherche n'existe pas"
        else:
            hey = "L'annonce a ete retire avec succes"
            Del_data(""Announcement"", ""Announcement_ID"", id)

    # Add a return statement for both GET and POST requests
    return render_template("Frontend/DeleteAn.html", hey=hey)


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
