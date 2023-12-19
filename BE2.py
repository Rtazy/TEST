from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg
from psycopg2 import sql
from flask import jsonify
from flask import session
import time
from datetime import datetime
import httpx
import base64

app = Flask(__name__)
# Define Supabase credentials directly in your code
supabase_url = "https://fnxcuzdjxvnmutcvhcqn.supabase.co"
supabase_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZueGN1emRqeHZubXV0Y3ZoY3FuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI0NzU1NzksImV4cCI6MjAxODA1MTU3OX0.8vBgJ3Iw9775FI1ATj1qb6dofMiVW3iobRM8myYTK8o"
app.secret_key='smth'



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
########################################
########################################
########################################\\

def insert_data_mobin(table_name, columns, column_values):
   conn= connect_db()
   cursor = conn.cursor()
    
            # Create an INSERT query with dynamic columns
   
   query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )

            # Execute the query with values
   cursor.execute(query, column_values)


    # Commit the transaction to persist changes
   conn.commit()

    # Close the cursor and connection when done
   cursor.close()
   connect_db().close()
 


def insert_data(table_name, maxvarbin_column, other_columns, binary_data, other_column_values):
    #####
            conn= connect_db()
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
            conn.commit()

    # Close the cursor and connection when done
            cursor.close()
            connect_db().close()
########################################
########################################
def select_entity(table,pkcol,entity_id):
            conn= connect_db()
            cursor = conn.cursor()
          

            query = f"SELECT * FROM {table} WHERE {pkcol} = {entity_id}"

            # Execute the query with the entity_id parameter
            cursor.execute(query)

            # Fetch the result
            entity = cursor.fetchone()

            return entity
########################################
########################################

def Del_data(table_name, primary_key_column, primary_key_value):
    conn= connect_db()
    cursor = conn.cursor()

    # Create an INSERT query with dynamic columns
    
    query = sql.SQL("DELETE FROM {} WHERE {}= %s").format(
        sql.Identifier(table_name), sql.Identifier(primary_key_column))


   # Execute the query with the primary key value
    cursor.execute(query, (primary_key_value,))

    # Commit the transaction to persist changes
    conn.commit()

    # Close the cursor and connection when done
    cursor.close()
    connect_db().close()
########################################
########################################

def Sel_data_one(table_name, primary_key_column, primary_key_value):
    conn= connect_db()
    cursor = conn.cursor()

    # Create an INSERT query with dynamic columns
    
    query = sql.SQL("SELECT * FROM {} WHERE {}= %s").format(
        sql.Identifier(table_name), sql.Identifier(primary_key_column))
 

   # Execute the query with the primary key value
    cursor.execute(query, (primary_key_value,))
    

    ret= cursor.fetchone()

    cursor.close()
    connect_db().close()
    return ret
########################################
def Sel_data_all(table_name, primary_key_column, primary_key_value):
    conn= connect_db()
    cursor = conn.cursor()

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
#################################################################
#################################################################
@app.route('/login', methods=['POST'])
def login():
    hey=""
    if request.method=='POST':
        email=request.form['email']
        passw=request.form['password']
        cursor=connect_db().cursor()
        cursor.execute('SELECT * FROM "Admin" WHERE "Email"=%s AND  "Password"=%s', email,passw)
        u=cursor.fetchone()
       
        if u != None:
            session['is_admin'] = True
            return render_template('admin_dashboard.html',hey)
        else:
            session['is_admin'] = False
            hey="Vos information sont incorrectes, veuillez reessayer ou cree un compte"
            return render_template('Frontend/login.html',hey=hey)

   
#################################################################
@app.route('/')
def pubp():

 return  render_template('Frontend/PublicPage.html')
#################################################################
@app.route('/dashboard')
def dashboard():
    # Check if the user is an admin before rendering the dashboard
    is_admin = session.get('is_admin', False)

    if is_admin:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for(''))
#################################################################
#################################################################

@app.route('/logout')
def logout():
    # Clear the session on logout
    session.clear()
    return redirect(url_for('index'))
#################################################################
#################################################################

@app.route('/Formulair',methods=['GET','POST'])
def Send_Form():
    if request.form['methods']==['GET','POST']:
       cat=request.form['cat']
      
       if cat is 1:
          redirect(url_for('Formulair_D'))
          
       elif cat is 2:
          redirect(url_for('Formulair_B'))
          
       elif cat is 3:
          redirect(url_for('Formulair_A'))
          
        
    return render_template('Form.html')

##### FORMS ######
@app.route("/Formulair_D", methods=["GET", "POST"])
def fill_fD():
    hey = ""
    try:
        if request.form['methods'] == ['POST']:
            Name = request.form['DonorName']
            Phone_Number=request.form['Phone_Number']
            Email = request.form['DonorEmail']
            gender = request.form['Gender']
            Address = request.files['Address']
            documents = request.files['DonorDocuments']
            joining_date = request.form['joining_date']
            b_date = request.form['DonorBirthDate']
            bdate_conv = datetime.strptime(b_date, "%d/%m/%Y").date()
            jdate_conv = datetime.strptime(joining_date, "%d/%m/%Y").date()
            docs_bin = documents.read()

            # Check if an image is provided
            if 'DonorImage' in request.files:
                donor_image = request.files['DonorImage']
                donor_image_conv = donor_image.read()
                img_url = insert_image_into_supabase("DonorImages", "Image", donor_image_conv)
            else:
                img_url = None

            Cols = ['Full_Name', 'Phone_Number', 'Email', 'Birthdate', 'Address', 'join_date', 'Gender', 'Image_URL']
            u = Select_entity("Donors", "Email", Email)

            if u is not None:
                hey = "Ce donneur existe déjà."
            else:
                # Insert data into the Donors table
                donor_id = insert_data("Donors", " Docs", Cols, [docs_bin, Name, Phone_Number, Email, bdate_conv,
                                                                  Address, jdate_conv, gender, img_url])
                hey = "Ce donneur a été ajouté avec succès avec l'ID : {}".format(donor_id)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("Frontend/error.html", error_message="An unexpected error occurred.")

    return render_template("Frontend/DonorForm.html", hey=hey)

@app.route("/Formulair_B", methods=["GET", "POST"])
def fill_fB():
    hey = ""
    try:
        if request.form["methods"] == ['GET', 'POST']:
            Name = request.form['BeneficiaryFullName']
            gender = request.form['Gender']
            Disability_Category = request.form['DisabilityType']
            documents = request.files['BeneficiaryDocuments']
            b_date = request.form['BeneficiaryBirthDate']
            b_place = request.form['Birthplace']
            Disability_sd = request.form['DisabilityDate']
            joining_date = request.files['joining_date']
            Disability_sd_con = datetime.strptime(Disability_sd, "%d/%m/%Y").date()
            bdate_conv = datetime.strptime(b_date, "%d/%m/%Y").date()
            jdate_conv = datetime.strptime(joining_date, "%d/%m/%Y").date()
            docs_bin = documents.read()

            # Check if an image is provided
            if 'BeneficiaryImage' in request.files:
                beneficiary_image = request.files['Picture']
                beneficiary_image_conv = beneficiary_image.read()
                img_url = insert_image_into_supabase("BeneficiaryImages", "Image", beneficiary_image_conv)
            else:
                img_url = None

            Cols = ['Full_Name', 'Birthdate', 'Birth_Place', 'join_date', 'Disability_Start_Date', 'Gender',
                    'Disability_Category', 'Image_URL']
            u = Select_entity("BenefForm", "Birthdate", b_date)
            hey = ""
            if u is not None:
                hey = "Ce membre existe déjà."
            else:
                # Insert data into the BenefForm table
                insert_data("BenefForm", " Documents", Cols, docs_bin,
                            [Name, bdate_conv, b_place, jdate_conv, Disability_sd_con, gender, Disability_Category,
                             img_url])
                hey = "Ce membre a été ajouté avec succès"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("Frontend/error.html", error_message="An unexpected error occurred.")

    return render_template('Frontend/BenForm.html', hey=hey)

#################################################################
#################################################################
     
@app.route("/Formulair_A",methods=["GET","POST"])
def fill_fA():
   hey=""
   if request.form['methods']==['POST']:
      c_name=request.form['AuthorityName']
      c_address=request.form['AuthorityAddress']
      c_email=request.form['Authorityemail']
      c_phoneN=request.form['AuthorityPhoneNumber']
      Join_Date = datetime.strptime(request.form['Join_Date'], "%d/%m/%Y")
      vals=[c_name,c_address,c_email,c_phoneN,Join_Date]
      u=Select_entity("Authorities","Email",c_email)
    
      if u!=None:
         hey="The authority already exists"
      else:
       insert_data_mobin('Authorities',['Name','Address','Email','Phone_Number','Join_Date'],vals)
       al="The authority was successfully added"
   return render_template("Frontend/AuthorityContactForm.html",hey=hey)  
          
#################################################################
def get_html(table):
    conn=connect_db()
    cursor=conn.cursor()

    query=f"SELECT * FROM  \"{table}\" "
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
# ... (previous code remains unchanged)

@app.route('/nouveau_beneficiere', methods=['POST', 'GET'])
def add_ben():
    print("Before form submission")
    hey = ""
    try:
        if request.method == 'POST':
            print("Before form submission")
            Name = request.form['Name']
            Join_Date = request.form['Join_Date']
            Benef_social_ID = request.form['beneficiaryId']
            b_date = request.form['Birthdate']
            b_place = request.form['Birth_Place']
            gender = request.form['gender']
            Disability_Category = request.form['Disability_Category']
            documents = request.files['documents']
            pic = request.files['picture']
            Disability_sd = request.form['Disability_startdate']

            Jdate_con = datetime.strptime(Join_Date, "%d/%m/%Y").date()
            Disability_sd_con = datetime.strptime(Disability_sd, "%d/%m/%Y").date()
            bdate_conv = datetime.strptime(b_date, '%d/%m/%Y').date()

            docs_bin = documents.read()
            pic_bin = pic.read()

            # Check if an image is provided
            if 'BeneficiaryImage' in request.files:
                beneficiary_image = request.files['BeneficiaryImage']
                beneficiary_image_conv = beneficiary_image.read()
                img_url = insert_image_into_supabase("BeneficiaryImages", "Image", beneficiary_image_conv)
            else:
                img_url = None

            # Check if a document is provided
            if 'BeneficiaryDocument' in request.files:
                beneficiary_document = request.files['BeneficiaryDocument']
                beneficiary_document_conv = beneficiary_document.read()
                doc_url = insert_document_into_supabase("BeneficiaryDocuments", "Document",
                                                        beneficiary_document_conv)
            else:
                doc_url = None

            Cols = ['Join_Date', 'Full_Name', 'Birthdate', 'Birth_Place', 'Disability_Start_Date', 'Gender',
                    'Disability_Category', 'Benef_social_ID', 'Image_URL', 'Document_URL']
            u = Select_entity('Beneficiaries', ['Full_Name', 'Birthdate', 'Birth_Place', 'Gender', 'Disability_Category',
                                                'Benef_social_ID'], [Name, bdate_conv, b_place, gender,
                                                                     Disability_Category, Benef_social_ID])

            if u is not None:
                hey = "Ce membre existe déjà."
            else:
                # Insert data into the Beneficiaries table
                beneficiary_id = insert_data("Beneficiaries", ['Documents', 'picture'], Cols,
                                            [docs_bin, pic_bin, Name, bdate_conv, b_place, Disability_sd_con, gender,
                                             Disability_Category, Benef_social_ID, img_url, doc_url])
                hey = "Ce membre a été ajouté avec succès avec l'ID : {}".format(beneficiary_id)
                print("afta form submission")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("Frontend/error.html", error_message="An unexpected error occurred.")

    return render_template('Frontend/ADDBenf.html', hey=hey)

# ... (remaining code remains unchanged)

########################################
########################################
# function for Adding an assosciation's contact
@app.route("/Ajouter_Sponsor",methods=['GET','POST'])
def add_Authority():
   hey=""
   if request.form['methods']==['POST']:
      c_name=request.form['AuthorityName']
      c_address=request.form['AuthorityAddress']
      c_email=request.form['Authorityemail']
      c_phoneN=request.form['AuthorityPhoneNumber']
      Join_Date = datetime.strptime(request.form['Join_Date'], "%d/%m/%Y")
      vals=[c_name,c_address,c_email,c_phoneN,Join_Date]
      u=Select_entity("Authorities","Email",c_email)
    
      if u!=None:
         hey="The authority already exists"
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

   return render_template("Frontend/add_us.html",hey=hey) 

########################################
########################################
# ... (previous code remains unchanged)

@app.route("/Ajouter_Campaingne", methods=['GET', 'POST'])
def add_Campaingn():
    hey = ""
    try:
        if request.method == 'POST':
            C_Title = request.form['title']
            C_Text = request.form['text']
            C_img = request.files['picture']
            C_startd = datetime.strptime(request.form['date'], "%d/%m/%Y")
            C_endd = datetime.strptime(request.form['e_date'], "%d/%m/%Y")
            C_img_conv = C_img.read()
            img_url = insert_image_into_supabase("Campaign", "Img", C_img_conv)

            insert_data_mobin("Campaign", ["Title", "Text", "start_date", "End_date", "img_url"],
                              [C_Title, C_Text, C_startd, C_endd, img_url])

        hey = "La campagne a été ajoutée avec succès."
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("Frontend/error.html", error_message="An unexpected error occurred.")

    return render_template("Frontend/CreateCam.html", hey=hey)

# ... (remaining code remains unchanged)

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
# ... (previous code remains unchanged)

@app.route("/Ajouter_Donneur", methods=['GET', 'POST'])
def add_Donor():
    hey = ""
    try:
        if request.method == 'POST':
            Name = request.form['Full_Name']
            Phone_Number=request.form['Phone_Number']
            Email = request.form['Email']
            gender = request.form['gender']
            Address = request.files['Address']
            documents = request.files['DonorDocuments']
            joining_date = request.form['join_date']
            b_date = request.form['BirthDate']
            bdate_conv = datetime.strptime(b_date, "%d/%m/%Y").date()
            jdate_conv = datetime.strptime(joining_date, "%d/%m/%Y").date()
            docs_bin = documents.read()

            # Check if an image is provided
            if 'DonorImage' in request.files:
                donor_image = request.files['DonorImage']
                donor_image_conv = donor_image.read()
                img_url = insert_image_into_supabase("DonorImages", "Image", donor_image_conv)
            else:
                img_url = None

            # Check if a document is provided
            if 'DonorDocument' in request.files:
                donor_document = request.files['DonorDocument']
                donor_document_conv = donor_document.read()
                doc_url = insert_document_into_supabase("DonorDocuments", "Document", donor_document_conv)
            else:
                doc_url = None

            Cols = ['Full_Name', 'Phone_Number', 'Email', 'Birthdate', 'Address', 'join_date', 'Gender', 'Image_URL', 'Document_URL']
            u = Select_entity("Donors", "Email", Email)
            if u is not None:
                hey = "Ce doneur existe déjà."
            else:
                # Insert data into the Donors table
                donor_id = insert_data("Donors", " Docs", Cols, docs_bin,[Name, Phone_Number, Email, bdate_conv, Address, jdate_conv, gender, img_url, doc_url])

                hey = "Ce doneur a été ajouté avec succès avec l'ID : {}".format(donor_id)
        return render_template("Frontend/ADDdonor.htm", hey=hey)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("Frontend/error.html", error_message="An unexpected error occurred.")

# ... (remaining code remains unchanged)

      
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


   return render_template("Frontend/Donation_mon.html") 
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

   return render_template("Frontend/Donation_oth.html") 

########################################
################################################


@app.route('/Retirer_Annonce', methods=['GET', 'POST'])
def Del_Ann():
    hey = ""
    tbl = to_htmltable(Sel_data_all2("Announcement"))
    if request.method == 'POST':
       
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
########################################
################################################

@app.route("/Ajouter_Annonce", methods=['GET', 'POST'])
def add_announcement():
    if request.method == 'POST':
        Ann_Title = request.form['title']
        Ann_Text = request.form['text']
        insert_data_mobin('Announcement', ['title', 'text'], [Ann_Title, Ann_Text])

    return render_template("Frontend/CreateAn.html") 
########################################
################################################
@app.route("/Retirer_contact",methods=['GET','POST'])
#first display contact list ..
def Del_Authority():
    hey = ""
    tbl = to_htmltable(Sel_data_all2("Authority"))
    if request.form['methods']==['POST']:
      A_id=request.form['SponsorId']
      ans = Select_entity("Authorities","Authority_ID", A_id) 
      
      if ans is None:
         hey="Le contact que vous avez selectionne n'existe pas"
      else:
         hey="Le contact que vous avez selectionne a ete retire"
         Del_data("Authorities","Authority_ID", A_id) 

    return render_template("Frontend/DeleteAuthority.html",tbl=tbl,hey=hey)
########################################
################################################
# Get Admin ID
@app.route("/View_Admin", methods=['POST', 'GET'])
def view_admin():
    hey = ""     
    tbl = to_htmltable(Sel_data_all2("Admin"))
    if request.method == 'POST':
        admin_id = request.form['adminId']
        

        if entity_data:
          entity_data = select_entity("Admin", "Admin_ID", admin_id)
        else:
            hey= f"No admin found with ID {admin_id}."
            

    return render_template("Frontend/ViewAdmin.html",tbl=tbl, hey=hey, entity_data=entity_data)
# Get Announcement ID
@app.route("/View_Announcement", methods=['POST', 'GET'])
def view_announcement():
    hey = ""     
    tbl = to_htmltable(Sel_data_all2("Announcement"))
    if request.method == 'POST':
        announcement_id = request.form['announcementId']
       

        if entity_data:
             entity_data = select_entity("Announcement", "Announcement_ID", announcement_id)
        else:
            hey = f"No announcement found with ID {announcement_id}."

    return render_template("Frontend/ViewAn.html", tbl=tbl, hey=hey, entity_data=entity_data)
# Get Campaign ID
@app.route("/View_Campaign", methods=['POST', 'GET'])
def view_campaign():
    if request.method == 'POST':
        hey = ""     
        tbl = to_htmltable(Sel_data_all2("Campaign"))
        campaign_id = request.form['campaignId']
        

        if entity_data:
            entity_data = select_entity("Campaign", "Campaign_ID", campaign_id) 
        else:
            hey = f"No campaign found with ID {campaign_id}."
             
    return render_template("Frontend/ViewCamp.html",tbl=tbl, hey=hey, entity_data=entity_data)
# Get Other Donation ID
@app.route("/View_Other_Donation", methods=['POST', 'GET'])
def view_other_donation():
    hey = ""     
    tbl = to_htmltable(Sel_data_all2("Other_Donation"))
    if request.method == 'POST':
        other_donation_id = request.form['otherDonationId']
       
        if entity_data:
            entity_data = select_entity("Other_Donation", "Donation_ID", other_donation_id)
 
        else:
           hey= f"No other donation found with ID {other_donation_id}."
           
    return render_template("Frontend/ViewDonation_oth.html",tbl=tbl, hey=hey, entity_data=entity_data)

# Get Monetary Donation ID
@app.route("/View_Monetary_Donation", methods=['POST', 'GET'])
def view_monetary_donation():
    hey = ""     
    tbl = to_htmltable(Sel_data_all2("Monetary_Donation"))
    if request.method == 'POST':
        monetary_donation_id = request.form['monetaryDonationId']
        entity_data = select_entity("Monetary_Donation", "Donation_ID", monetary_donation_id)

        if entity_data is None:
            hey = f"No monetary donation found with ID {monetary_donation_id}."
           
    return render_template("Frontend/ViewDonation_mon.html",tbl=tbl, hey=hey, entity_data=entity_data)
@app.route("/View_Donor", methods=['GET', 'POST'])
def view_donor():
    hey = ""
    tbl = to_htmltable(Sel_data_all2("Donors"))

    if request.method == 'POST':
        D_id = request.form['donorId']
        entity_data = select_entity("Donors", "Donor_ID", D_id)

        if entity_data is None:
            hey = "The selected donor does not exist."
        else:
            hey = "The selected donor information:"

    return render_template("Frontend/ViewDonor.html", tbl=tbl, hey=hey, entity_data=entity_data)

# Authorities
@app.route("/View_Authority", methods=['GET', 'POST'])
def view_authority():
    hey = ""
    tbl = to_htmltable(Sel_data_all2("Authorities"))

    if request.method == 'POST':
        A_id = request.form['authorityId']
        entity_data = select_entity("Authorities", "Authority_ID", A_id)

        if entity_data is None:
            hey = "The selected authority does not exist."
        else:
            hey = "The selected authority information:"

    return render_template("Frontend/ViewAuthority.html", tbl=tbl, hey=hey, entity_data=entity_data)




########################################
def update_data(table_name, entity_id, columns, new_values):
    current_data = select_entity(table_name, entity_id)
    for column in columns:
        new_value = new_values.get(column, None)
        if new_value is not None:
            current_data[column] = new_value
    update_data_in_db(table_name, entity_id, current_data)
    return render_template('update_success.html', entity=table_name)

def update_data_with_image(table_name, entity_id, columns, new_values, image_column, image_data):
    current_data = select_entity(table_name, entity_id)
    for column in columns:
        new_value = new_values.get(column, None)
        if new_value is not None:
            current_data[column] = new_value
    update_data_in_db(table_name, entity_id, current_data)
    insert_image_into_supabase(table_name, image_column, image_data)
    return render_template('update_success.html', entity=table_name)

# Update a donor's information
@app.route('/update_donor/<donor_id>', methods=['POST'])
def update_donor(donor_id):
    new_values = request.form.to_dict()
    return update_data('Donors', donor_id, ['Full_Name', 'Phone_Number', 'Email', 'Birthdate', 'Address', 'join_date', 'Gender'], new_values)

# Update a beneficiary's information
@app.route('/update_beneficiary/<beneficiary_id>', methods=['POST'])
def update_beneficiary(beneficiary_id):
    new_values = request.form.to_dict()
    return update_data('BenefForm', beneficiary_id, ['Full_Name', 'Birthdate', 'Birth_Place', 'join_date', 'Disability_Start_Date', 'Gender', 'Disability_Category'], new_values)

# Update an authority's information
@app.route('/update_authority/<authority_id>', methods=['POST'])
def update_authority(authority_id):
    new_values = request.form.to_dict()
    return update_data_mobin('Authorities', authority_id, ['Name', 'Address', 'Email', 'Phone_Number', 'Join_Date'], new_values)

# Update an announcement's information
@app.route('/update_announcement/<announcement_id>', methods=['POST'])
def update_announcement(announcement_id):
    new_values = request.form.to_dict()
    return update_data_mobin('Announcement', announcement_id, ['title', 'text'], new_values)

# Update a campaign's information
@app.route('/update_campaign/<campaign_id>', methods=['POST'])
def update_campaign(campaign_id):
    new_values = request.form.to_dict()
    return update_data_mobin('Campaign', campaign_id, ['Title', 'Text', 'start_date', 'End_date'], new_values)

# Update a monetary donation's information
@app.route('/update_monetary_donation/<monetary_donation_id>', methods=['POST'])
def update_monetary_donation(monetary_donation_id):
    new_values = request.form.to_dict()
    return update_data_mobin('Monetary_Donation', monetary_donation_id, ['owner_ID', 'Amount', 'Payment_method', 'is_association'], new_values)

# Update an other donation's information
@app.route('/update_other_donation/<other_donation_id>', methods=['POST'])
def update_other_donation(other_donation_id):
    new_values = request.form.to_dict()
    image_data = request.files.get('image').read() if 'image' in request.files else None
    if image_data:
        return update_data_with_image('Other_Donation', other_donation_id, ['owner_ID', 'Description', 'is_association'], new_values, 'image_column_name', image_data)
    else:
        return update_data_mobin('Other_Donation', other_donation_id, ['owner_ID', 'Description', 'is_association'], new_values)

################################################
def update_data_in_db(table_name, entity_id, data):
    conn = connect_db()
    cur = conn.cursor()

    # Generate the SET clause for the SQL query
    set_clause = ', '.join(f'"{column}" = %s' for column in data.keys())

    # Construct and execute the SQL query
    sql_query = f'UPDATE "{table_name}" SET {set_clause} WHERE "id" = %s'
    cur.execute(sql_query, list(data.values()) + [entity_id])

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def update_data_mobin(table_name, entity_id, columns, values):
    conn = connect_db()
    cur = conn.cursor()

    # Generate the SET clause for the SQL query
    set_clause = ', '.join(f'"{column}" = %s' for column in columns)

    # Construct and execute the SQL query
    sql_query = f'UPDATE "{table_name}" SET {set_clause} WHERE "id" = %s'
    cur.execute(sql_query, values + [entity_id])

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

@app.route('/Gestion')
def profile():
    return render_template("Frontend/Manager.html")

if __name__ == '__main__':
    app.run(debug=True)
