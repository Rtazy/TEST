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
#################################################################
@app.route('/dashboard')
def dashboard():
    # Check if the user is an admin before rendering the dashboard
    is_admin = session.get('is_admin', False)

    if is_admin:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('index'))
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

@app.route("/Formulair_D",methods=["GET","POST"])
def fill_fD():
   hey=""
   if request.form['methods']==['POST']:
     sid=request.form['DonorSID']
     Name=request.form['DonorName']
     Email=request.form['DonorEmail']
     gender=request.form['Gender']
     pnum=request.form['DonorPhone']
     Address=request.files['Address']
     documents=request.files['DonorDocuments']
     joining_date=request.form['joining_date']
     b_date=request.form['DonorBirthDate']
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
     return render_template("Frontend/DonorForm.html",hey=hey)
       
@app.route("/Formulair_B",methods=["GET","POST"])
def fill_fB():
  hey=""
  if request.form["methods"]==['GET','POST']: 
     Name=request.form['BeneficiaryFullName']
     gender=request.form['Gender']
     Disability_Category=request.form['DisabilityType']
     documents=request.files['BeneficiaryDocuments']
     b_date=request.form['BeneficiaryBirthDate']
     b_place=request.form['Birthplace']
     Disability_sd=request.form['DisabilityDate']
     pic=request.files['Picture']
     Disability_sd_con=datetime.strptime(Disability_sd,"%d/%m/%Y").date()
     bdate_conv=datetime.strptime(b_date,"%d/%m/%Y").date()
     jdate_conv=datetime.strptime(joining_date,"%d/%m/%Y").date()
     docs_bin= documents.read()
     Cols=['Full_Name','Birthdate','Birth_Place','join_date','Disability_Start_Date','Gender','Disability_Category' ]
     u=Select_entity("BenefForm","Birthdate",b_date)
     hey=""
     if u != None:
        hey="Ce membre exist deja."
     else:
         insert_data("BenefForm", " Documents" ,Cols, docs_bin,[Name, bdate_conv, b_place,jdate_conv,Disability_sd_con,gender,Disability_Category] )
         hey="Ce membre a ete ajoute"
   
     return render_template('Frontend/BenForm.html',hey=hey)   
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

    conn=connect_db()
    cursor = conn.cursor()

    query = sql.SQL("DELETE FROM {} WHERE {} = %s").format(
        sql.Identifier(table_name),
        sql.Identifier(key_column)
    )

    cursor.execute(query, (key_value,))
  
    conn.commit()
    cursor.close()
    conn.close()
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
   hey=""
   if request.form['methods']==['POST']:
     Name=request.form['Full_Name']
     Email=request.form['Email']
     gender=request.form['gender']
     Address=request.files['Address']
     documents=request.files['DonorDocuments']
     joining_date=request.form['join_date']
     b_date=request.form['BirthDate']
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
        tbl = to_htmltable(Sel_data_all2("Donors"))
    if request.method == 'POST':
        admin_id = request.form['adminId']
        entity_data = select_entity("Admin", "Admin_ID", admin_id)

        if entity_data:
          entity_data = select_entity("Donors", "Donor_ID", D_id) 
        else:
            hey= f"No admin found with ID {admin_id}."
            

    return render_template("Frontend/ViewAdmin.html",tbl=tbl, hey=hey, entity_data=entity_data)
# Get Announcement ID
@app.route("/View_Announcement", methods=['POST', 'GET'])
def view_announcement():
        hey = ""     
        tbl = to_htmltable(Sel_data_all2("Donors"))
    if request.method == 'POST':
        announcement_id = request.form['announcementId']
        entity_data = select_entity("Announcement", "Announcement_ID", announcement_id)

        if entity_data:
             entity_data = select_entity("Donors", "Donor_ID", D_id) 
        else:
            hey = f"No announcement found with ID {announcement_id}."
            return render_template("Frontend/ViewCamp.html, message=message)

    return render_template("Frontend/ViewAn.html", tbl=tbl, hey=hey, entity_data=entity_data)
# Get Campaign ID
@app.route("/View_Campaign", methods=['POST', 'GET'])
def view_campaign():
    if request.method == 'POST':
            hey = ""     
            tbl = to_htmltable(Sel_data_all2("Donors"))
        campaign_id = request.form['campaignId']
        entity_data = select_entity("Campaign", "Campaign_ID", campaign_id)

        if entity_data:
            entity_data = select_entity("Donors", "Donor_ID", D_id) 
        else:
            hey = f"No campaign found with ID {campaign_id}."
             

    return render_template("Frontend/GetCampaignId.html",tbl=tbl, hey=hey, entity_data=entity_data)
# Get Other Donation ID
@app.route("/View_Other_Donation", methods=['POST', 'GET'])
def view_other_donation():
        hey = ""     
        tbl = to_htmltable(Sel_data_all2("Donors"))
    if request.method == 'POST':
        other_donation_id = request.form['otherDonationId']
        entity_data = select_entity("Other_Donation", "Donation_ID", other_donation_id)

        if entity_data:
             entity_data = select_entity("Donors", "Donor_ID", D_id) 
        else:
           hey= f"No other donation found with ID {other_donation_id}."
           
    return render_template("Frontend/GetOtherDonationId.html",tbl=tbl, hey=hey, entity_data=entity_data)

# Get Monetary Donation ID
@app.route("/View_Monetary_Donation", methods=['POST', 'GET'])
def view_monetary_donation():
        hey = ""     
        tbl = to_htmltable(Sel_data_all2("Monetary_Donation"))
    if request.method == 'POST':
        monetary_donation_id = request.form['monetaryDonationId']
        entity_data = select_entity("Monetary_Donation", "Donation_ID", monetary_donation_id)

        if entity_data:
           entity_data = select_entity("Donors", "Donor_ID", D_id) 
        else:
            message = f"No monetary donation found with ID {monetary_donation_id}."
           
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
################################################

@app.route('/Gestion')
def profile():
    return render_template("Frontend/Manager.html")

if __name__ == '__main__':
    app.run(debug=True)
