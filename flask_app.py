from flask import Flask, redirect, render_template, session, request
from os import urandom
import sqlite3
import deck
index = -1
Deck = []
Deck = deck.CreateDeck(Deck)
Deck = deck.ShuffleDeck(Deck)

app = Flask(__name__)

app.secret_key = urandom(16)

@app.route('/')
def index():
    if not session.get('username'):
        return redirect('/login')
    return render_template('index.html')

@app.route('/create')
def create():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute(	"""	CREATE TABLE Users(
					Username VARCHAR(20) NOT NULL PRIMARY KEY,
					Password VARCHAR(20) NOT NULL
						  )
			""")
	con.commit()
	return 'CREATE'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("INSERT INTO Users (Username, Password) VALUES (?,?)",
                    (request.form['username'],request.form['password']))
    con.commit()
    session['username'] = request.form.get('username')
    return redirect('/')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    con = sqlite3.connect('login.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE Username=? AND Password=?",
                    (request.form['username'],request.form['password']))
    match = len(cur.fetchall())
    if match == 0:
        return 'Wrong username and password'
    else:
        session['username'] = request.form.get('username')
        return redirect('/')

@app.route('/select')
def select():
	con = sqlite3.connect('login.db')
	cur = con.cursor()
	cur.execute('SELECT * FROM Users')
	rows = cur.fetchall()
	return str(rows)

@app.route('/hands')
def hands():
    if not session.get('username'):
        return redirect('/login')
    return render_template('hands.html')

@app.route('/rules')
def rules():
    if not session.get('username'):
        return redirect('/login')
    return render_template('rules.html')

@app.route('/play')
def play():
    if not session.get('username'):
        return redirect('/login')
    return render_template('play.html')
def home():
    return str(index) + " : " + str(deck.GetCard(Deck, index))

@app.route('/account')
def account():
    if not session.get('username'):
        return redirect('/login')
    return render_template('account.html')

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')