import os

from secret import databaseKey
from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, RegisterForm
from models import User


from models import db, connect_db

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://postgres:' + databaseKey + '@localHost:5432/TheFridge'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route('/')
def index():
    return render_template("index.html")

def do_login(user):
    """Stores user in session"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Deletes user from Session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def check_user_creds():
    """Checks for user in session and returns to index if not"""
    if not g.user:
        flash("You must be logged in to continue", "danger")
        return redirect("/")

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles user login"""
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.validate(form.username.data,form.password.data)

        if user:
            do_login(user)
            return redirect("/home")

        flash("Invalid credentials.", 'danger')

    return render_template("login.html", form=form)

@app.route("/logout" , methods=["GET"])
def logout():
    """Calls logout function then redirects to index"""

    do_logout()
    return redirect('/')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handles user register and adds them to the database"""
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                profile_image=form.profile_image.data or User.profile_image.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/home")

    else:
        return render_template('signup.html', form=form)

@app.route("/home", methods=["GET"])
def home():
    """Home page for logged in users"""

    check_user_creds()


    return render_template("home.html")
    
