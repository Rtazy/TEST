from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg
from psycopg2 import sql
from flask import jsonify
import time
from datetime import datetime
#fetchmany
#fetchone
#fetchall these come afer "execute"
#functions needed add: comp y ,admin yy, ben yy, auth yy, don yy, ev,an yy,donation yy,forms yes|

app= Flask(__name__)
app.config['DB_USER']='rimetazi_AlNour'
app.config['DB_NAME']='rimetazi_AlNour'
app.config['DB_HOST']='sql.bsite.net\MSSQL2016'
app.config['DB_PASSWORD']='1202'

#insert Querries:VARBINARY(MAX) is the data type for imgs,pdfs .. .







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
   return pg.connect(host=app.config['DB_HOST'],dbname=app.config['DB_NAME'],user=app.config['DB_USER'],password=app.config['DB_PASSWORD'])


########################################\\

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


    # Commit the transaction to persist changes
   connect_db().commit()

    # Close the cursor and connection when done
   cursor.close()
   connect_db().close()
 


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
    return err
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
  if request.form["methods"]==['GET','POST']: 
     Name=request.form['Name']
     Phone_Number=request.form['Phone_Number']
     Email=request.form['Email']
     gender=request.form['Gender']
     Address=request.files['Address']
     documents=request.files['Docs']
     joining_date=request.form['joining_date']
     b_date=request.form['Birthdate']
     bdate_conv=datetime.strptime(b_date,'%Y-%m-%d').date()
     jdate_conv=datetime.strptime(joining_date,'%Y-%m-%d').date()
     docs_bin= documents.read()
     Cols=['Full_Name','Phone_Number','Email','Birthdate','Address','join_date','Gender' ]
     u=Select_entity("Donors","Email",Email)
     hey=""
     if u != None:
        hey="Ce doneur exist deja."
     else:
        insert_data("Donors", " Docs" ,Cols, docs_bin,[Name,Phone_Number,Email, bdate_conv,Address,jdate_conv,gender] )
        hey="Ce doneur a ete ajoute"
   
  return render_template('DonorForm.html')   
  
@app.route("/Formulair_B",methods=["GET","POST"])
def fill_fB():
  if request.form["methods"]==['GET','POST']: 
     Name=request.form['Name']
     gender=request.form['gender']
     Disability_Category=request.form['Disability_Category']
     documents=request.files['documents']
     joining_date=request.form['joining_date']
     b_date=request.form['Birthdate']
     b_place=request.form['Birth_Place']
     Disability_sd=request.form['Disability_startdate']
     Disability_sd_con=datetime.strptime(Disability_sd,'%Y-%m-%d').date()
     bdate_conv=datetime.strptime(b_date,'%Y-%m-%d').date()
     jdate_conv=datetime.strptime(joining_date,'%Y-%m-%d').date()
     docs_bin= documents.read()
     Cols=['Full_Name','Birthdate','Birth_Place','join_date','Disability_Start_Date','Gender','Disability_Category' ]
     u=Select_entity("BenefForm","Birthdate",b_date)
     hey=""
     if u != None:
        hey="Ce membre exist deja."
     else:
         insert_data("BenefForm", " Documents" ,Cols, docs_bin,[Name, bdate_conv, b_place,jdate_conv,Disability_sd_con,gender,Disability_Category] )
         hey="Ce membre a ete ajoute"
   
     return render_template('BenForm.html')   
     
@app.route("/Formulair_A",methods=["GET","POST"])
def fill_fA():
  if request.form["methods"]==['GET','POST']: 
      c_name=request.form['Name']
      c_address=request.form[' Address']
      c_email=request.form['Email ']
      c_phoneN=request.form['Phone_Number']
      Join_Date=request.form['Join_Date']
      Join_Date_conv=datetime.strtime(Join_Date,"%Y-%m-%d")
      vals=[c_name,c_address,c_email,c_phoneN,Join_Date_conv]
      u=Select_entity("AuthoritiesForm","Email",c_email)
      al=""
      if u!=None:
         al="The authority already exists"
      else:
       insert_data_mobin('AuthoritiesForm',['Name','Address','Email','Phone_Number','Join_Date'],vals)
       al="The authority was successfully added"
  return render_template('AuthorityContactForm.html')   
          
#################################################################
@app.route('/Home',methods=['POST','GET'])
def Home():

    return render_template('PublicPage.html')


@app.route('/Connexion',methods=['POST','GET'])
def login():
    if request.form['methods']=='POST':
        email=request.form['email']
        passw=request.form['pass']
        cursor=connect_db().cursor()
        cursor.execute('SELECT* FROM users WHERE email=%s AND pass=%s', email,passw)
        u=cursor.fetchone()
        hey=""
        if u:

            redirect(url_for('profile_<username>'))
        else:
            hey="Vos information sont incorrectes, veuillez reessayer ou cree un compte"
    return render_template('login.html',hey=hey)
        
################ profile
@app.route('/profile')
def profile():
 return render_template('Manager.html')

################ add

#Function for adding a user  There should also be a function to add users from the forms 
#three retractable tables will be displayed 
@app.route('/nouveau_beneficiere',methods=['POST','GET'])
def add_ben():
    if request.form['methods']==['POST']:
  
     Name=request.form['Name']
     gender=request.form['gender']
     Disability_Category=request.form['Disability_Category']
     documents=request.files['documents']
     joining_date=request.form['joining_date']
     b_date=request.form['Birthdate']
     b_place=request.form['Birth_Place']
     Disability_sd=request.form['Disability_startdate']
     Disability_sd_con=datetime.strptime(Disability_sd,'%Y-%m-%d').date()
     bdate_conv=datetime.strptime(b_date,'%Y-%m-%d').date()
     jdate_conv=datetime.strptime(joining_date,'%Y-%m-%d').date()
     docs_bin= documents.read()
     Cols=['Full_Name','Birthdate','Birth_Place','join_date','Disability_Start_Date','Gender','Disability_Category' ]
     u=Select_entity()
     hey=""
     if u != None:
        hey="Ce membre exist deja."
     else:
         insert_data("Beneficiaries", " Documents" ,Cols, docs_bin,[Name, bdate_conv, b_place,jdate_conv,Disability_sd_con,gender,Disability_Category] )
         hey="Ce membre a ete ajoute"
   
    return render_template('add_member.html',hey)
# function for Adding an assosciation's contact
@app.route("/Ajouter_Contact",methods=['GET','POST'])
def add_Authority():
   if request.form['methods']==['POST']:
      c_name=request.form['Name']
      c_address=request.form[' Address']
      c_email=request.form['Email ']
      c_phoneN=request.form['Phone_Number']
      Join_Date=request.form['Join_Date']
      Join_Date_conv=datetime.strtime(Join_Date,"%Y-%m-%d")
      vals=[c_name,c_address,c_email,c_phoneN,Join_Date_conv]
      u=Select_entity("Authorities","Email",c_email)
      al=""
      if u!=None:
         al="The authority already exists"
      else:
       insert_data_mobin('Authorities',['Name','Address','Email','Phone_Number','Join_Date'],vals)
       al="The authority was successfully added"
   return render_template("add_Auth.html") 

@app.route("/Ajouter_Administrateur",methods=['GET','POST'])
#the original admin must be connected  to do that
def add_admin():
   if request.form['methods']==['POST']:
      use_name=request.form['Admin_Name']
      use_address=request.form['Address']
      use_email=request.form['Email']
      use_phoneN=request.form['use_phoneN']
      use_pw=request.form['Password']
      u=Select_entity("Admin","Email",use_email)

       
   hey=""
   if u != None:
         hey="L'administrateur que vous essayer d'ajouter existe deja "
   else:
         hey="L'administrateur a ete ajoute avec succes"
         insert_data_mobin("Admin",[ 'Admin_Name','Admin_PhoneNumber', 'Address TEXT','Email','Password'],[use_name,use_phoneN,use_address,use_email,use_pw])

   return render_template("add_us.html",hey =hey) 

@app.route("/Ajouter_Campaingne",methods=['GET','POST'])

def add_Campaingn():
   if request.form['methods']==['POST']:
      C_Title=request.form['Title']
      C_Text=request.form['Text']
      C_img= request.files['Image']
      C_startd=datetime.strtime(request.form['Start_date'],"%Y-%m-%d")
      C_endd=datetime.strtime(request.form['Start_date'],"%Y-%m-%d")
      C_img_conv=C_img.read()
      insert_data("Campaign","Img",[ "Title","Text","start_date","End_date"],C_img_conv,[C_Title,C_Text,C_startd,C_endd])
   return render_template("add_Camp.html") 


@app.route("/Ajouter_Annonce",methods=['GET','POST'])

def add_announcement():
   if request.form['methods']==['POST']:
      Ann_Title=request.form['title']
      Ann_Text=request.form['text']
      insert_data_mobin('Announcement',['title','text'],[Ann_Title,Ann_Text,])

   return render_template("add_ann.html") 

#add donor and add donation (Shouldn't we allow donors to sign up??)
@app.route("/Ajouter_Doneur",methods=['GET','POST'])
#the original admin must be connected  to do that
def add_Donor():
   if request.form['methods']==['POST']:
     Name=request.form['Name']
     Phone_Number=request.form['Phone_Number']
     Email=request.form['Email']
     gender=request.form['Gender']
     Address=request.files['Address']
     documents=request.files['Docs']
     joining_date=request.form['joining_date']
     b_date=request.form['Birthdate']
     bdate_conv=datetime.strptime(b_date,'%Y-%m-%d').date()
     jdate_conv=datetime.strptime(joining_date,'%Y-%m-%d').date()
     docs_bin= documents.read()
     Cols=['Full_Name','Phone_Number','Email','Birthdate','Address','join_date','Gender' ]
     u=Select_entity("Donors","Email",Email)
     hey=""
     if u != None:
        hey="Ce doneur exist deja."
     else:
        insert_data("Donors", " Docs" ,Cols, docs_bin,[Name,Phone_Number,Email, bdate_conv,Address,jdate_conv,gender] )
        hey="Ce doneur a ete ajoute"
      

   return render_template("add_Don.html",hey=hey) 
  
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


#Function for deleting a use

#Function for modifying a user profile(Category, Documents

# Function for donating 



# function for Deleting a Beneficiary from the beneficiary table 
# function for Deleting a Beneficiary from the beneficiary table 
@app.route('/Retirer_Beneficiere',methods=['GET','POST'])
def Del_ben():
   if request.form['methods']==['POST']:
      # first display the table of benfs and the user has to display their ids

      A_id=request.form['Beneficiary_ID ']
      
      ans = Select_entity("Beneficiaries","Beneficiary_ID ", A_id) 
      if ans==None:
         alert="Le beneficiere que vous avez selectionne n'existe pas"
      else:
         ans = Del_data("Beneficiaries","Beneficiary_ID ", A_id) 
         alert="Le beneficiere que vous avez selectionne a ete retire"
   return render_template("del_ben.html",alert)


@app.route('/Retirer_Admin',methods=['GET','POST'])
def Del_Admin():
   if request.form['methods']==['POST']:
      id=request.form['Admin_ID']
      res=Select_entity("Admin","Admin_ID",id)
      al=""
      if res == None:
         al="L' Admin que vous avez recherche n'existe pas"
      else :
         al="L' Admin a ete retire avec succes"
         Del_data("Admin","Admin_ID",id)
   return render_template("del_admin.html",al)

# function for Deleting a Campaign from the Campaign table 
@app.route('/Retirer_Campagne',methods=['GET','POST'])
def Del_Comp():
   if request.form['methods']==['POST']:
      id=request.form['Campaign_ID']
      res=Select_entity("Campaign","Campaign_ID",id)
      al=""
      if res == None:
         al="La campagne que vous avez recherche n'existe pas"
      else :
         al="La campagne a ete retire avec succes"
         Del_data("Campaign","Campaign_ID",id)
   return render_template("del_cam.html",al)


@app.route("/Retirer_Doneurs",methods=['POST',"GET"])
def  Del_Donor():
   if request.form['methods']==['POST']:
      id=request.form['Donors_ID']
      res=Select_entity("Donors","Donors_ID",id)
      al=""
      if res == None:
         al="Le doneur que vous avez recherche n'existe pas"
      else :
         al="Le doneur a ete retire avec succes"
         Del_data("Donors","Donors_ID",id)
   return render_template("del_don.html",al)


# trigger on off when a campaign is deleted an announcement is autaumatically created
# deleting an announcement:
@app.route('/Retirer_Annonce',methods=['GET','POST'])
def Del_Ann():
   if request.form['methods']==['POST']:
      # first display the table of benfs and the user has to display their ids
      id=request.form['Announcement_ID']
      res=Select_entity("Announcement","Announcement_ID",id)
      al=""
      if res == None:
         al="L'annonce que vous avez recherche n'existe pas"
      else :
         al="L'annonce a ete retire avec succes"
         Del_data("Announcement","Announcement_ID",id)

   return render_template("del_ann.html",al)
# function for Deleting a Beneficiary from beneficiary forms (add trigger) 

# function for Deleting an assosciation's contact
@app.route("/Retirer_contact",methods=['GET','POST'])
#first display contact list ..
def Del_Authority():
   if request.form['methods']==['POST']:
      A_id=request.form['Authority_ID']
      ans = Select_entity("Authorities","Authority_ID", A_id) 
      
      if ans==1:
         alert="Le contact que vous avez selectionne n'existe pas"
      else:
         alert="Le contact que vous avez selectionne a ete retire"
         Del_data("Authorities","Authority_ID", A_id) 

      return render_template("del_Auth.html",alert=alert)
   
@app.route("/Retirer_Don",methods=['GET','POST'])
#first display Donation list ..
def Del_Don():
   if request.form['methods']==['POST']:
      Don_id=request.form['Don_id']
      Don_type=request.form['Don_type']
      
   if Don_type == 1:
       con=Select_entity("Monetary_Donation","Donation_ID",Don_id)
       
       alert=""
       if con==None:
         alert="Le Don que vous avez selectionne n'existe pas"
       else:
         Del_data("Monetary_Donation","Donation_ID",Don_id)
         alert="le don a ete suprime avec succes"
   elif Don_type == 2:
       con=Select_entity("Other_Donation","Donation_ID",Don_id)
       
       alert=""
       if con==None:
         alert="Le Don que vous avez selectionne n'existe pas"
       else:
         Del_data("Other_Donation","Donation_ID",Don_id)
         alert="le don a ete suprime avec succes"


   return render_template("del_donation.html") 
###########################################################
@app.route('/update_beneficiary', methods=['GET', 'POST'])
def update_beneficiary_input_id():
    if request.method == 'POST':
        beneficiary_id = request.form.get('beneficiary_id')
        return redirect(url_for('update_beneficiary_route', beneficiary_id=beneficiary_id))
    else:
        return render_template('input_beneficiary_id.html')
   ##
@app.route('/update_beneficiary/<int:beneficiary_id>', methods=['GET', 'POST'])
def update_beneficiary_route(beneficiary_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'Full_Name': request.form.get('Full_Name', ''),
            'Birthdate': request.form.get('Birthdate', ''),
            'Birth_Place': request.form.get('Birth_Place', ''),
            'Disability_category': request.form.get('Disability_category', ''),
            'Disability_Start_Date': request.form.get('Disability_Start_Date', ''),
            'Gender': request.form.get('Gender', ''),
            'Join_Date': request.form.get('Join_Date', '')
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Beneficiary
        try:
            update_beneficiary(beneficiary_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    beneficiary = Select_entity("Beneficiaries", "Beneficiary_ID", beneficiary_id)
    return render_template('update_beneficiary.html', beneficiary=beneficiary, hey=hey)

###########################################################
@app.route('/update_authority', methods=['GET', 'POST'])
def update_authority_input_id():
    if request.method == 'POST':
        authority_id = request.form.get('authority_id')
        return redirect(url_for('update_authority_route', authority_id=authority_id))
    else:
        return render_template('input_authority_id.html')

@app.route('/update_authority/<int:authority_id>', methods=['GET', 'POST'])
def update_authority_route(authority_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'Name': request.form.get('Name', ''),
            'Address': request.form.get('Address', ''),
            'Email': request.form.get('Email', ''),
            'Phone_Number': request.form.get('Phone_Number', ''),
            'Join_Date': request.form.get('Join_Date', '')
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Authority
        try:
            update_authority(authority_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    authority = Select_entity("Authorities", "Authority_ID", authority_id)
    return render_template('update_authority.html', authority=authority, hey=hey)
###########################################################
@app.route('/update_campaign', methods=['GET', 'POST'])
def update_campaign_input_id():
    if request.method == 'POST':
        campaign_id = request.form.get('campaign_id')
        return redirect(url_for('update_campaign_route', campaign_id=campaign_id))
    else:
        return render_template('input_campaign_id.html')

@app.route('/update_campaign/<int:campaign_id>', methods=['GET', 'POST'])
def update_campaign_route(campaign_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'Title': request.form.get('Title', ''),
            'Text': request.form.get('Text', ''),
            'start_date': request.form.get('start_date', ''),
            'End_date': request.form.get('End_date', ''),
            # Add more attributes as needed
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Campaign
        try:
            update_campaign(campaign_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    campaign = Select_entity("Campaign", "Campaign_ID", campaign_id)
    return render_template('update_campaign.html', campaign=campaign, hey=hey)
###########################################################
def update_announcement_input_id():
    if request.method == 'POST':
        announcement_id = request.form.get('announcement_id')
        return redirect(url_for('update_announcement_route', announcement_id=announcement_id))
    else:
        return render_template('input_announcement_id.html')

@app.route('/update_announcement/<int:announcement_id>', methods=['GET', 'POST'])
def update_announcement_route(announcement_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'title': request.form.get('title', ''),
            'txt': request.form.get('txt', ''),
            # Add more attributes as needed
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Announcement
        try:
            update_announcement(announcement_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    announcement = Select_entity("Announcement", "Announcement_ID", announcement_id)
    return render_template('update_announcement.html', announcement=announcement, hey=hey)

###########################################################
@app.route('/update_monetary_donation', methods=['GET', 'POST'])
def update_monetary_donation_input_id():
    if request.method == 'POST':
        donation_id = request.form.get('donation_id')
        return redirect(url_for('update_monetary_donation_route', donation_id=donation_id))
    else:
        return render_template('input_monetary_donation_id.html')

@app.route('/update_monetary_donation/<int:donation_id>', methods=['GET', 'POST'])
def update_monetary_donation_route(donation_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'owner_ID': request.form.get('owner_ID', ''),
            'Amount': request.form.get('Amount', ''),
            'Payment_method': request.form.get('Payment_method', ''),
            'is_association': request.form.get('is_association', ''),
            # Add more attributes as needed
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Monetary Donation
        try:
            update_monetary_donation(donation_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    donation = Select_entity("Monetary_Donation", "Donation_ID", donation_id)
    return render_template('update_monetary_donation.html', donation=donation, hey=hey)
###########################################################
@app.route('/update_other_donation', methods=['GET', 'POST'])
def update_other_donation_input_id():
    if request.method == 'POST':
        donation_id = request.form.get('donation_id')
        return redirect(url_for('update_other_donation_route', donation_id=donation_id))
    else:
        return render_template('input_other_donation_id.html')

@app.route('/update_other_donation/<int:donation_id>', methods=['GET', 'POST'])
def update_other_donation_route(donation_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'owner_ID': request.form.get('owner_ID', ''),
            'Description': request.form.get('Description', ''),
            'is_association': request.form.get('is_association', ''),
            # Add more attributes as needed
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Other Donation
        try:
            update_other_donation(donation_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    donation = Select_entity("Other_Donation", "Donation_ID", donation_id)
    return render_template('update_other_donation.html', donation=donation, hey=hey)
###########################################################
@app.route('/update_donor', methods=['GET', 'POST'])
def update_donor_input_id():
    if request.method == 'POST':
        donor_id = request.form.get('donor_id')
        return redirect(url_for('update_donor_route', donor_id=donor_id))
    else:
        return render_template('input_donor_id.html')

@app.route('/update_donor/<int:donor_id>', methods=['GET', 'POST'])
def update_donor_route(donor_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'Full_Name': request.form.get('Full_Name', ''),
            'Phone_Number': request.form.get('Phone_Number', ''),
            'Email': request.form.get('Email', ''),
            'Join_Date': request.form.get('Join_Date', ''),
            'Birthdate': request.form.get('Birthdate', ''),
            'Address': request.form.get('Address', ''),
            # Add more attributes as needed
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Donor
        try:
            update_donor(donor_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    donor = Select_entity("Donors", "Donor_ID", donor_id)
    return render_template('update_donor.html', donor=donor, hey=hey)
###########################################################
@app.route('/update_admin', methods=['GET', 'POST'])
def update_admin_input_id():
    if request.method == 'POST':
        admin_id = request.form.get('admin_id')
        return redirect(url_for('update_admin_route', admin_id=admin_id))
    else:
        return render_template('input_admin_id.html')

@app.route('/update_admin/<int:admin_id>', methods=['GET', 'POST'])
def update_admin_route(admin_id):
    hey = ""
    if request.method == 'POST':
        update_data = {
            'Admin_Name': request.form.get('Admin_Name', ''),
            'Admin_PhoneNumber': request.form.get('Admin_PhoneNumber', ''),
            'Address': request.form.get('Address', ''),
            'Email': request.form.get('Email', ''),
            'Password': request.form.get('Password', ''),
            # Add more attributes as needed
        }

        # Remove empty values from the update_data dictionary
        update_data = {k: v for k, v in update_data.items() if v}

        # Update the Admin
        try:
            update_admin(admin_id, update_data)
            hey = "Update successful!"
        except Exception as e:
            hey = f"Update failed: {str(e)}"

    admin = Select_entity("Admin", "Admin_ID", admin_id)
    return render_template('update_admin.html', admin=admin, hey=hey)
###########################################################

@app.route("/Retirer_Formulaire",methods=['GET','POST'])

def Del_Form():
   if request.form['methods']==['POST']:
      Form_id=request.form['Don_id']
      Form_type=request.form['Don_type']
      
      if Form_type == 1:
       con=Select_entity("DonorForm","Form_ID",Form_id)
       
       alert=""
       if con==None:
         alert="le formulair de contact que vous avez selectionne n'existe pas"
       else:
         Del_data("AuthoritiesForm","DonorForm_ID",Form_id)
         alert="le formulair de contact a ete suprime avec succes"
   elif Form_type == 2:
       con=Select_entity("BenfForm","Form_ID",Form_id)
       
       alert=""
       if con==None:
         alert="le formulair de beneficiere que vous avez selectionne n'existe pas"
       else:
         Del_data("BenForm","rForm_ID",Form_id)
         alert="le formulair de beneficiere a ete suprime avec succes"
   elif Form_type == 3:
       con=Select_entity("DonorForm","Form_ID",Form_id)
       
       alert=""
       if con==None:
         alert="Le formulair de doneur que vous avez selectionne n'existe pas"
       else:
         Del_data("DonorForm","Form_ID",Form_id)
         alert="le formulair de doneur a ete suprime avec succes"



   return render_template("del_Form.html") 




 #  E X T R A
    #auto post Ai after each scheduled event
    #  Data Analitics part
    # how will the donors donate? go get funding campain
    # how to make sure that the user donated the correct amount?
 

if __name__=='__main__':
    app.run(debug=True)
