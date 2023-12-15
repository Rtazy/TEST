from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg
from psycopg2 import sql
from flask import jsonify
import time
from datetime import datetime
import httpx
import base64

app = Flask(__name__)
# Define Supabase credentials directly in your code
supabase_url = "https://fnxcuzdjxvnmutcvhcqn.supabase.co"
supabase_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZueGN1emRqeHZubXV0Y3ZoY3FuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI0NzU1NzksImV4cCI6MjAxODA1MTU3OX0.8vBgJ3Iw9775FI1ATj1qb6dofMiVW3iobRM8myYTK8o"




# Load configuration from a separate file (config.py)
app.config.from_pyfile('config.py', silent=True)


conn_string = (
    f"postgresql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}@"
    f"{app.config['DB_HOST']}/{app.config['DB_NAME']}?sslmode=require")


async def insert_image_into_supabase(table_name, column_name, image_data):
    # Encode image data as base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    url = f"{supabase_url}/table/{table_name}"

    # Set up headers with the Supabase API key
    headers = {
        "Content-Type": "application/json",
        "apikey": supabase_api_key,
    }

    # Construct the request payload
    payload = {
        column_name: encoded_image,
    }

    async with httpx.AsyncClient() as client:
        # Make the request to insert the image
        response = await client.post(url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 201:
            # Return the inserted image's ID
            return response.json().get('id')
        else:
            # Handle the error case (you may want to raise an exception or handle it differently)
            print(f"Failed to insert image. Status code: {response.status_code}")
            return None

async def insert_document_into_supabase(table_name, column_name, document_data):
    # Encode document data as base64
    encoded_document = base64.b64encode(document_data).decode('utf-8')

    # Construct the Supabase URL
    url = f"{supabase_url}/table/{table_name}"

    # Set up headers with the Supabase API key
    headers = {
        "Content-Type": "application/json",
        "apikey": supabase_api_key,
    }

    # Construct the request payload
    payload = {
        column_name: encoded_document,
    }

    async with httpx.AsyncClient() as client:
        # Make the request to insert the document
        response = await client.post(url, headers=headers, json=payload)

        # Check if the request was successful
        if response.status_code == 201:
            # Return the inserted document's ID
            return response.json().get('id')
        else:
            # Handle the error case (you may want to raise an exception or handle it differently)
            print(f"Failed to insert document. Status code: {response.status_code}")
            return None

def to_htmltable(data):
    res = '<table border="1">'
    
    if data:
        colspan = len(data[0])
        
        for row in data:
            res += '<tr>'
            for col in row:
                res += '<td>'
                res += str(col)
                res += '</td>'
            res += '</tr>'
    else:
        colspan = 1
        res += '<tr><td colspan="{}">No data available</td></tr>'.format(colspan)
    
    res += '</table>'
    return res





@app.route('/api/get_html')
def get_html(table):
    conn=connect_db()
    cursor=conn.cursor()

    query=f"SELECT * FROM  \"{table}\" WHERE \"{key}\"={id} "
    data=cursor.execute(query) 
    return jsonify({'html': to_htmltable(data)})
    #


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
          

            query = f'SELECT * FROM "{table}" WHERE "{pkcol}" = {entity_id}'

            # Execute the query with the entity_id parameter
            cursor.execute(query)

            # Fetch the result
            entity = cursor.fetchone()

            return entity
########################################
########################################

def Del_data(table_name, key_column, key_value):
    try:
        cursor = connect_db().cursor()
        query = f"DELETE FROM \"{table_name}\" WHERE \"{key_column}\" = %s"
        print("Query:", query)  # Add this line
        cursor.execute(query, key_value)
        connect_db().commit()
    except Exception as e:
        print("Error:", e)  # Add this line for error logging
    finally:
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
     Jdate_con=datetime.strptime(request.form['jdate'],"%d/%m/%Y").date()
     Disability_sd_con = datetime.strptime(Disability_sd, "%d/%m/%Y").date()
     bdate_conv=datetime.strptime(b_date,'%d/%m/%Y').date()
     docs_bin= documents.read()
     Pic_bin= pic.read()
     Cols=['Join_Date','Full_Name','Birthdate','Birth_Place','Disability_Start_Date','Gender','Disability_Category' ,'Benef_social_ID']
     u=Select_entity('Beneficiary',['Full_Name','Birthdate','Birth_Place','Gender','Disability_Category'],[Name,bdate_conv, b_place, gender,Disability_Category,Benef_social_ID] )
     
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
   return render_template("Frontend/AddAuthority.html",hey=hey) 

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

   return render_template("Frontend/add_us.html") 

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
            img_url = insert_image_into_supabase("Campaign", "Img", C_img_conv)

            insert_data_mobin("Campaign", ["Title", "Text", "start_date", "End_date","img_url"], [C_Title, C_Text, C_startd, C_endd,img_url])
        return render_template("Frontend/CreateCam.html")
    except Exception as e:        
        print(f"An error occurred: {str(e)}")
        return render_template("Frontend/error.html", error_message="An unexpected error occurred.")
########################################get_data(querry)
########################################
@app.route("/Retirer_Doneur", methods=['POST', 'GET'])
def Del_Donor():
    hey = ""
    if request.method == 'POST':
        donor_id = request.form['DonorId']
        res = Select_entity("Donors", "Donors_ID", donor_id)
        
        if res is None:
            hey = "Le donneur que vous avez recherche n'existe pas"
        else:
            hey = "Le donneur a ete retire avec succes"
            Del_data("Donors", "Donors_ID", donor_id)

    return render_template("Frontend/DeleteDonor.html", hey=hey)
################################################
########################################

@app.route("/Ajouter_Donneur",methods=['GET','POST'])
#the original admin must be connected  to do that
def add_Donor():
   if request.form['methods']==['POST']:
     Name=request.form['Full_Name']
     Email=request.form['Email']
     gender=request.form['Gender']
     Address=request.files['Address']
     documents=request.files['DonorDocuments']
     joining_date=request.form['joining_date']
     b_date=request.form['Birthdate']
     bdate_conv=datetime.strptime(b_date,"%d/%m/%Y").date()
     jdate_conv=datetime.strptime(joining_date,"%d/%m/%Y").date()
     docs_bin= documents.read()
     Cols=['Full_Name','Phone_Number','Email','Birthdate','Address','join_date','Gender' ]
     u=Select_entity("Donors","Email",Email)
     hey=""
     if u != None:
        hey="Ce doneur exist deja."
     else:
        insert_data("Donors", " Docs" ,Cols, docs_bin,[Name,Phone_Number,Email, bdate_conv,Address,jdate_conv,gender] )
        hey="Ce doneur a ete ajoute"
     return render_template("Frontend/ADDdonor.htm",hey=hey) 
      
########################################
################################################

  
@app.route("/Ajouter_Donation_argent",methods=['GET','POST'])
def add_Don_M():
   if request.form['methods']==['POST']:
      Don_owner=request.form['owner_ID']
      Don_Amount=request.form['Amount']
      pm=request.form['Payment_method']
      is_a=request.form['is_association']
      cols=['owner_ID','Amount','Payment_method','is_association']
      vals=[Don_owner,Don_Amount,pm,is_a]
      insert_data_mobin('Monetary_Donation',cols,vals)


   return render_template("Donation_mon.html") 
########################################
################################################
@app.route("/Ajouter_Donation_autre",methods=['GET','POST'])
def add_Don_o():
   if request.form['methods']==['POST']:
      Don_owner=request.form['owner_ID']
      
      Desc=request.form['Description']
      is_a=request.form['is_association']
      cols=['owner_ID','Amount','Payment_method','is_association']
      vals=[Don_owner,Desc,is_a]
      insert_data_mobin('Other_Donation',cols,vals)

   return render_template("Donation_oth.html") 

########################################
################################################


@app.route('/Retirer_Annonce', methods=['GET', 'POST'])
def Del_Ann():
    hey = ""
    tbl = ""
    if request.method == 'POST':
        tbl = to_htmltable(Sel_data_all2("Announcement"))

        id = request.form['announcementId']

        # Check if the announcement with the provided ID exists
        res = Select_entity("Announcement", "Announcement_ID", id)

        if res is None:
            hey = "L'annonce que vous avez recherche n'existe pas"
        else:
            try:
                # Attempt to delete the announcement
                Del_data('Announcement', 'Announcement_ID', id)
                hey = "L'annonce a ete retire avec succes"
            except Exception as e:
                # Log the exception for debugging
                print(f"Error during deletion: {e}")
                hey = "Une erreur s'est produite lors de la suppression de l'annonce."

    return render_template("Frontend/DeleteAn.html", hey=hey, tbl=tbl)

@app.route("/Ajouter_Annonce", methods=['GET', 'POST'])
def add_announcement():
    if request.method == 'POST':
        Ann_Title = request.form['title']
        Ann_Text = request.form['text']
        insert_data_mobin('Announcement', ['title', 'text'], [Ann_Title, Ann_Text])

    return render_template("Frontend/CreateAn.html")


@app.route('/Gestion')
def profile():
    return render_template("Frontend/Manager.html")

if __name__ == '__main__':
    app.run(debug=True)
