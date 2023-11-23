from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg
#fetchmany
#fetchone
#fetchall these come afer "execute"

app= Flask(__name__)
app.config['DB_USER']='postgres'
app.config['DB_NAME']='Alnour'
app.config['DB_HOST']='postgres'
app.config['DB_PASSWORD']='1202'

#insert Querries:VARBINARY(MAX) is the data type for imgs,pdfs .. .

insert_auth="SELECT Authority_Name,Authority_id  FROM Authorities WHERE Authority_Name=%s OR Authority_id=%s"
insert_use="INSERT INTO users(fname,lname,category,cin) VALUES (%s,%s,%s,%s)"
insert_camp=""
insert_ben=""
insert_ann=""
insert_Dform=""
insert_Aform=""
insert_Bform=""
insert_NDonation=""
insert_Mdonation=""

del_auth=""
del_use=""
del_camp=""
del_ben=""
del_ann=""
del_form=""
del_NDonation=""
del_MDonation=""

up_auth=""
up_use=""
up_camp=""
up_ben=""
up_ann=""
up_form=""
up_NDonation=""
up_Mdonation=""





#create the code in HTML for ajax:

def to_htmltable(lst):
   
   for item in lst:
     res+='<td>'

     for tem in item:
         res+="<tb>{}</tb>".format(tem)
     res+='</td>'
              
   return res

def display(querry):

   res=connect_db.cursor().execute(querry).fetchall()
   return to_htmltable(res)

#send the code to AJAX?? 



def connect_db():
   return pg.connect(host=app.config['DB_HOST'],dbname=app.config['DB_NAME'],user=app.config['DB_USER'],password=app.config['DB_PASSWORD'])

@app.route('/Hey',methods=['GET','POST'])
def index():
    
    return '''<form method="post" action="/submit"> <label for="user_in">Enter username</label> <input type="input" name="username" id="user_in"> <input type="submit" name="submit"> </form>'''
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
          

       ##interactive?? js or I can use redirect




    #  if request.method=='POST':
    #    username=request.form['username']
       #   passw=request.form['pass']
         # email=request.form['email']
         # phone=request.form['phone']
         # cat=request.form['category']
         # cursor=connect_db.cursor()
         # cursor.execute("SELECT * FROM forms WHERE username=%s OR email=%s",username,email)
         # row=cursor.fetchone()
         # if row==None: 
          # cursor.execute("INSERT INTO users(username,pass,email,phone,category) (%s,%s,%s,%s,%s)",username,passw,email,phone,cat)
          # connect_db.commit()
          # connect_db.close()
          # hey=""
          # return redirect(url_for('login'))
         # else:
          # hey="Les informations que vous venez rentre existent deja dans la base de donnees. Connecter vous ou change l'address E-mail ou le nom d'utilisateur"
        
    return render_template('Form.html')

##### FORMS ######

@app.route("/Formulair_D",methods=["GET","POST"])
def fill_fD():
  if request.form["methods"]==['GET','POST']: 
   cur=connect_db.cursor()
   Donor_Name=request.form['dname']
   Donor_address=request.form['daddres']
   Donor_address=request.form['dname']
   Donor_address=request.form['dname']
   cur.execute(insert_Dform, )
   return render_template('DonorForm.html')   
  
@app.route("/Formulair_B",methods=["GET","POST"])
def fill_fB():
  if request.form["methods"]==['GET','POST']: 
   cur=connect_db.cursor()
   B_name=request.form['name']
   B_bday=request.form['BirthDate']
   B_phone=request.form['phoneNumber']
   B_address=request.form['address']
   B_pic=request.form['picture']
   B_Doc=request.form['document']
   B_Disability=request.form['disabilityType']
   cur.execute(insert_Bform,)
   
   return render_template('BenForm.html')   
     
@app.route("/Formulair_A",methods=["GET","POST"])
def fill_fA():
  if request.form["methods"]==['GET','POST']: 
   cur=connect_db.cursor()
   A_name=request.form['Aname']
   A_address=request.form['bname']
   A_address=request.form['bname']
   A_address=request.form['Aname']
   cur.execute(insert_Aform, )
   return render_template('AuthorityContactForm.html')   
          
#################################################################
@app.route('/Home',methods=['POST','GET'])
def login():
    if request.form['methods']=='POST':
        email=request.form['email']
        passw=request.form['pass']
        cursor=connect_db.cursor()
        cursor.execute('SELECT* FROM users WHERE email=%s AND pass=%s', email,passw)
        u=cursor.fetchone()
        hey=""
        if u:

            redirect(url_for('profile_<username>'))
        else:
            hey="Vos information sont incorrectes, veuillez reessayer ou cree un compte"
    return render_template('PublicPage.html')


@app.route('/Connexion',methods=['POST','GET'])
def login():
    if request.form['methods']=='POST':
        email=request.form['email']
        passw=request.form['pass']
        cursor=connect_db.cursor()
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
def add_member():
    if request.form['methods']==['POST']:
     fname=request.form['fname']
     lname=request.form['lname']
     category=request.form['category']
     cin=request.form['cin']
     cur=connect_db.cursor()
     cur.execute("SELECT *FROM users WHERE %s=cin")
     u=cur.fetchone()
     hey=""
     if u != None:
        hey="Ce membre exist deja."
     else:
        cur.execute(insert_use,fname,lname,category,cin)
        hey="Ce membre a ete ajoute"
     connect_db.commit()
     connect_db.close()
    return render_template('add_member.html',hey)
# function for Adding an assosciation's contact
@app.route("/Ajouter_Contact",methods=['GET','POST'])
def add_Authority():
   if request.form['methods']==['POST']:
      c_name=request.form['c_name']
      c_address=request.form['c_address']
      c_email=request.form['c_email']
      c_phoneN=request.form['c_phoneN']
      cur=connect_db.cursor()
      
      cur.execute("INSERT INTO Authority(c_name,c_address,c_email,c_phoneN) VALUES (%s,%s,%s,%s)",c_name,c_address,c_email,c_phoneN)
      connect_db.commit()
      connect_db.close()

   return render_template("add_Auth.html") 
@app.route("/Ajouter_Administrateur",methods=['GET','POST'])
#the original admin must be connected  to do that
def add_use():
   if request.form['methods']==['POST']:
      use_name=request.form['use_name']
      use_address=request.form['use_address']
      use_email=request.form['use_email']
      use_phoneN=request.form['use_phoneN']
      cur=connect_db.cursor()
      cur.execute(sel_us,)
      ath=cur.fetchone()
      hey=""
      if ath != None:
         hey="L'administrateur que vous essayer d'ajouter existe deja "
      else:
         hey="L'administrateur a ete ajoute avec succes"
         cur.execute(insert_use, )
         connect_db.commit()
         connect_db.close()

   return render_template("add_us.html",hey=hey) 

@app.route("/Ajouter_Annonce",methods=['GET','POST'])

def add_announcement():
   if request.form['methods']==['POST']:
      Ann_Title=request.form['Ann_name']
      Ann_Text=request.form['Ann_address']
      cur=connect_db.cursor()
      ath=cur.fetchone()
      cur.execute(insert_ann, )
      connect_db.commit()
      connect_db.close()

   return render_template("add_ann.html",hey=hey) 

#add donor and add donation (Shouldn't we allow donors to sign up??)
@app.route("/Ajouter_Doneur",methods=['GET','POST'])
#the original admin must be connected  to do that
def add_Don():
   if request.form['methods']==['POST']:
      Don_name=request.form['Don_name']
      Don_address=request.form['Don_address']
      Don_email=request.form['Don_email']
      Don_phoneN=request.form['Don_phoneN']
      Don_Docs=request.form['Don_docs']
      cur=connect_db.cursor()
      cur.execute( sel_don,)
      ath=cur.fetchone()
      hey=""
      if ath != None:
         hey="L'administrateur que vous essayer d'ajouter existe deja "
      else:
         hey="L'administrateur a ete ajoute avec succes"
         cur.execute(insert_don, )
         connect_db.commit()
         connect_db.close()

   return render_template("add_Don.html",hey=hey) 
  
@app.route("/Ajouter_Donation_argent",methods=['GET','POST'])
def add_Don():
   if request.form['methods']==['POST']:
      Don_name=request.form['Don_name']
      Don_address=request.form['Don_address']

      cur=connect_db.cursor()
      cur.execute(insert_don, )
      connect_db.commit()
      connect_db.close()

   return render_template("Donation_mon.html",hey=hey) 
@app.route("/Ajouter_Donation_autre",methods=['GET','POST'])
def add_Don():
   if request.form['methods']==['POST']:
      Don_name=request.form['Don_name']
      Don_address=request.form['Don_address']

      cur=connect_db.cursor()
      
      cur.execute(insert_dona_o, )
      connect_db.commit()
      connect_db.close()

   return render_template("Donation_oth.html") 


#Function for deleting a use

#Function for modifying a user profile(Category, Documents

# Function for donating 



# function for Deleting a Beneficiary from the beneficiary table 
@app.route('/Retirer_Beneficiere',methods=['GET','POST'])
def Del_ben():
   if request.form['methods']==['POST']:
      # first display the table of benfs and the user has to display their ids
      id=request.form['id']
      cur=connect_db.cursor()
      cur.execute(sel_ben,)
      res=cur.fetchone()
      al=""
      if al == None:
       al="Le beneficiere que vous avez recherche n'existe pas"
      else :
        al="Le beneficiere a ete retire avec succes"
        cur.execute(del_ben,)
        connect_db.commit()
        connect_db.close()
   return render_template("del_ben.html",al)

# function for Deleting a Campaign from the Campaign table 
@app.route('/Retirer_Campagne',methods=['GET','POST'])
def Del_ben():
   if request.form['methods']==['POST']:
      # first display the table of benfs and the user has to display their ids
      id=request.form['id']
      cur=connect_db.cursor()
      cur.execute(sel_cam,)
      res=cur.fetchone()
      al=""
      if al == None:
         al="La Campagne que vous avez recherche n'existe pas"
       else :
         al="La Campagne a ete retire avec succes"
         cur.execute(del_ben,)
         connect_db.commit()
         connect_db.close()
   return render_template("del_cam.html",al)
# trigger on off when a campaign is deleted an announcement is autaumatically created
# deleting an announcement:
@app.route('/Retirer_Annonce',methods=['GET','POST'])
def Del_Ann():
   if request.form['methods']==['POST']:
      # first display the table of benfs and the user has to display their ids
      id=request.form['id']
      cur=connect_db.cursor()
      cur.execute(sel_ann,)
      res=cur.fetchone()
      al=""
      if al == None:
         al="L'annonce que vous avez recherche n'existe pas"
      else :
         al="L'annonce a ete retire avec succes"
         cur.execute(del_ann,)
         connect_db.commit()
         connect_db.close()
   return render_template("del_ann.html",al)
# function for Deleting a Beneficiary from beneficiary forms (add trigger) 

# function for Deleting an assosciation's contact
@app.route("/Retirer_contact",methods=['GET','POST'])
#first display contact list ..
def Del_Authority():
   if request.form['methods']==['POST']:
      A_id=request.form['A_id']
      cur=connect_db.cursor()
      cur.execute("SELECT Authority_id  FROM Authorities WHERE Authority_id=%s",)
      con=cur.fetchone()
      alert=""
      if con==None:
         alert="Le contact que vous avez selectionne n'existe pas"
      else:
       # ask the user whether they would like to delete the contact
       approves=True
       if approves:
          cur.execute("DELETE FROM Authorities WHERE Authority_id=%s",A_id)
          connect_db.commit()
      
      connect_db.close()

   return render_template("del_Auth.html") 


@app.route("/Retirer_Don",methods=['GET','POST'])
#first display Donation list ..
def Del_Authority():
   if request.form['methods']==['POST']:
      Don_id=request.form['Don_id']
      Don_type=request.form['Don_type']
      cur=connect_db.cursor()
      if Don_type == 1:
       cur.execute()
       con=cur.fetchone()
       alert=""
       if con==None:
         alert="Le Don que vous avez selectionne n'existe pas"
       else:
         cur.execute(del_NDonation,A_id)
         connect_db.close()
         alert="le don a ete suprime avec succes"
   elif Don_type == 2:
       cur.execute()
       con=cur.fetchone()
       alert=""
       if con==None:
         alert="Le Don que vous avez selectionne n'existe pas"
       else:
         cur.execute(del_MDonation,A_id)
         connect_db.commit()
         connect_db.close()
         alert="le don a ete suprime avec succes"



   return render_template("del_Auth.html") 

 #  E X T R A
    #auto post Ai after each scheduled event
    #  
 

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)