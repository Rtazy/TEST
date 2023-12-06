from flask import Flask


app= Flask(__name__)
app.config['DB_USER']='rimetazi_AlNour'
app.config['DB_NAME']='rimetazi_AlNour'
app.config['DB_HOST']='sql.bsite.net\MSSQL2016'
app.config['DB_PASSWORD']='1202'

def connect_db():
   return pg.connect(host=app.config['DB_HOST'],dbname=app.config['DB_NAME'],user=app.config['DB_USER'],password=app.config['DB_PASSWORD'])


@app.route('/profile')
def profile():
    return 'Hello, this is a test response from the /profile route!'

if __name__ == '__main__':
    app.run(debug=True)
