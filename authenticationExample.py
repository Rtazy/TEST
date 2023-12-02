from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Simulated user data (replace this with your authentication logic)
users = {
    'admin': 'password123',
}

# Variable to track whether a user is logged in
logged_in = False

@app.route('/public')
def public_page():
    return render_template('public.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            logged_in = True
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
   #can't be accessed unless the user logged in
    if not logged_in:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
