from flask import Flask, render_template, request, redirect, url_for,session
from db import Database
import sqlite3

app = Flask(__name__)
app.secret_key='1234'

# Initialize the single database with both tables
db = Database('twitty.db')
db.create_tables()  # Create both tweets and users tables

@app.route("/")
def home():
    alert = request.args.get('alert')  # Get alert message from query params
    return render_template('main.html', alert=alert)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form.get('text', '')
    return redirect(url_for('search', text=text))

@app.route("/search")
def search():
    text = request.args.get('text', '')
    results = db.search_data('tweets', text) if text else []
    return render_template('search.html', text=text, results=results)


@app.route("/newtweet")
def newtweet():
    return render_template('newtweet.html')

@app.route("/accept", methods=['POST'])
def accept_tweet():
    text = request.form['text']
    db.insert_data('tweets', (text,))
    return f'You entered: {text}'

@app.route("/tweets")
def tweets():
    tweets = db.get_data('tweets')
    return render_template('tweets.html', tweets=tweets)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        try:
            db.register_user(username, email, password)
            return redirect(url_for('login'))  
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Username or email already exists.")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.verify_user(username, password):
            session['logged_in'] = True  # Set session variable
            return redirect(url_for('home', alert='You logged in'))  # Redirect with alert message
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')


@app.route("/accept", methods=['POST'])
def my_form_post_2():
    text = request.form['text']
    db.insert_data('tweets', (text,))  # Only insert tweet text now
    return redirect(url_for('tweets'))# Redirect with alert

if __name__ == "__main__":
    app.run(debug=True)
