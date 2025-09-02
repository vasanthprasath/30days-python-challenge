
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sih2025'

# Database setup
def init_db():
    conn = sqlite3.connect('farmers.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    query TEXT NOT NULL,
                    response TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Register
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # farmer or expert
        try:
            conn = sqlite3.connect('farmers.db', check_same_thread=False)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (username, password, role))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists!"
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('farmers.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = user[0]
            session['role'] = user[3]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('farmers.db', check_same_thread=False)
    c = conn.cursor()
    if session['role'] == 'farmer':
        c.execute("SELECT * FROM queries WHERE user_id=?", (session['user'],))
    else:  # expert
        c.execute("SELECT * FROM queries")
    queries = c.fetchall()
    conn.close()
    return render_template('dashboard.html', queries=queries, role=session['role'])

# Submit Query
@app.route('/submit_query', methods=['POST'])
def submit_query():
    query_text = request.form['query']
    user_id = session['user']
    conn = sqlite3.connect('farmers.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO queries (user_id, query, response) VALUES (?,?,?)", (user_id, query_text, ''))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# Respond to Query
@app.route('/respond/<int:query_id>', methods=['POST'])
def respond(query_id):
    response_text = request.form['response']
    conn = sqlite3.connect('farmers.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE queries SET response=? WHERE id=?", (response_text, query_id))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
