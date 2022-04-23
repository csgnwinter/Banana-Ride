from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Message, Mail


# Define database
db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = "lift.ride.hailing@gmail.com"
app.config["MAIL_PASSWORD"] = "tom&jerry"
mail = Mail(app)


# Initialise
def create_app():

    # Defining the maximum time to live
    app.permanent_session_lifetime = timedelta(minutes=5)

    # Configuring the database
    app.config['SECRET_KEY'] = 'F&LukE.XX3M3mCG=_P)C:P~g+$;.m-u)HZ,4+Pzv4!%(ys^Eo.SE(<Ex<%o#Si'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Tell the program the available blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')       # Url_prefix points to which def function to go to in views.py
    app.register_blueprint(auth, url_prefix='/')        # Url_prefix points to which def function to go to in auth.py

    from .models import User
    create_database(app)

    # Redirects if user is not logged in
    # Redirects users to auth.py login if user is not logged in
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


# Checks if database exists and if it doesn't, it will generate one
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')


