# Define imports
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from Website.hashing import checkPassword, hashPasswordEncrypt
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Set up blueprint for flask application
auth = Blueprint('auth', __name__)


# /login called by html in base.html
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':                    # If the user clicks on the button, it will enter this if statement
        username = request.form.get('username')     # Get the data from the textbox and store into username
        password = request.form.get('password')     # Get the data from the textbox and store into password

        user = User.query.filter_by(username=username).first()      # Extract username based on input username

        if user:                                                    # Checks if user exists in the DB
            if checkPassword(user.password, password):              # Validates the password
                login_user(user, remember=True)                     # Using external modules flask_login to store user
                session.permanent = True                            # Ensuring the program will log out if user did not use the program for a certain time
                session['username'] = username                      # Storing the data in username into a session variable
                return redirect(url_for('views.home'))              # Redirect to views.py home, pass variable username
            else:
                flash('Incorrect password. Please try again.', category='error')        # If password don't match, flash an error message
        else:                                                       # If the user does not exist in the DB
            flash('Username does not exist.', category='error')     # If username doesn't match, show error message

    return render_template("login.html", user=current_user, username="")


# /logout called by html in base.html
@auth.route('/logout')
@login_required                                 # Make sure we cannot access this page unless the user is logged in
def logout():
    session.pop('username', None)               # Remove the data in the session by using pop
    logout_user()                               # Using external modules to log user out
    return redirect(url_for('auth.login'))      # Returned to auth.py for another login


# /sign-up called by html in base.html
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':                        # If the user clicks on the button, it will enter this if statement
        username = request.form.get('username')         # Get the value of the user input and store into the variable
        password1 = request.form.get('password1')       # Get the value of the user input and store into the variable
        password2 = request.form.get('password2')       # Get the value of the user input and store into the variable

        user = User.query.filter_by(username=username).first()          # Checks if the input username exists in the database
        if user:                                                        # If it exists, enter the if statement
            flash('Username already exist!', category='error')          # Print an error message
        elif len(username) < 4:                                                         # Validation, ensure length of username more than 4
            flash('Username must be greater than 3 characters!', category='error')      # If len < 4, print error message
        elif password1 != password2:                                                    # If password and confirm password, not same
            flash('Password don\'t match!', category='error')                           # Print error message
        elif len(password1) < 7:                                                        # If password len lesser than 7,
            flash('Password must be at least 7 characters!', category='error')          # Print error message
        else:
            new_user = User(username=username, password=hashPasswordEncrypt(password1))     # Store input data into an object new_user
            db.session.add(new_user)                                                        # Add the data into the db session
            db.session.commit()                                                             # Commit the changes
            login_user(new_user, remember=True)                                             # Use the flask login to add a user into login_user
            flash('Account created!', category='success')                                   # Prints success message
            return redirect(url_for('auth.login'))                                          # Once success message, redirect to views.py HOME, pass username value
    return render_template("sign_up.html", user=current_user)
