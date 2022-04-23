# custom class
from flask_login import UserMixin
from . import db


# Set up TransactionOrders model
class TransactionOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True)                # Auto generated id value for each transaction order, PK
    pickUpLocation = db.Column(db.Integer)                      # Creating a column for storing pick up location data
    dropOffLocation = db.Column(db.Integer)                     # Creating a column for storing drop off location data
    numOfPassengers = db.Column(db.Integer)                     # Creating a column for storing num of passengers data
    costPrice = db.Column(db.Float)                             # Creating a column for storing cost price data
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # Link each row to the corresponding data in User table


# Set up user model
# UserMixin use for User object only
# UserMixin works with flask_login current users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)                # Auto generated id value for each user
    username = db.Column(db.String(150), unique=True)           # Creating a column for storing username
    password = db.Column(db.String(150))                        # Creating a column for storing password
    transactionOrder = db.relationship('TransactionOrders')     # Establish foreign relationship with TransactionOrders model