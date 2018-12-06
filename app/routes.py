from flask import render_template
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Jason'}
    return render_template("home.html", user = user)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)