from flask import Flask, render_template, request, redirect, url_for
import psycopg2 as pg
#fetchmany
#fetchone
#fetchall these come afer "execute"

def connect_db():
   return pg.connect(host='localhost',dbname='postgres',user='postgres',password='1202')

cur=connect_db().cursor()
cur.execute("SELECT * FROM one")
res=cur.fetchall()
print(type(res))
print(type(res[0]))

#create the code in HTML:

def to_htmltable(lst):
   
   for item in lst:
     res+='<td>'

     for tem in item:
         res+="<tb>{}</tb>".format(tem)
     res+='</td>'
              
   return res

# what language was I supposed to use???

