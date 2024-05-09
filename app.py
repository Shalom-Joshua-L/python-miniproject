from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create SQLite database and tables for users and expenses
conn = sqlite3.connect('expenses.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, category TEXT, description TEXT, date TEXT)''')
conn.commit()

# Function to handle user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("Both username and password are required!", "error")
        else:
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('login'))
    return render_template('signup.html')

# Function to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("Both username and password are required!", "error")
        else:
            conn = sqlite3.connect('expenses.db')
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            conn.close()
            if user:
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password!", "error")
    return render_template('login.html')

# Placeholder dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)