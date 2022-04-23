# Define roots
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from .functions import mapSearch, nodeDistance, distancePricing, surge, matching_panda
from .shortestRoute import MapInit
from .models import TransactionOrders
from . import db
from flask_mail import Message, Mail
from .__init__ import mail
import pandas as pd

# Set up blueprint for flask application
views = Blueprint('views', __name__)
startHeader = "Welcome, "
endHeader = "!"


def updateBook(driverLocation):
    df = pd.read_csv('Website/driver.csv')
    df.loc[(df['current_lat'] == driverLocation[0]) & (df['current_long'] == driverLocation[1]),'isBooked'] = 1
    df.to_csv('Website/driver.csv', index=False)


@views.route('/', methods=['GET', 'POST'])
@login_required                                 # This detects if user is logged in, cannot get to this root page unless logged in
def home():
    if "username" in session:                   # Checks if the username is in session
        username = session['username']          # If true, get the data from the session and store into variable
    else:
        return redirect(url_for('auth.login'))  # Else, will be redirected to login page

    if request.method == 'POST':                # If user clicks on the button in HTML
        startingLocation = request.form.get('startingLocation')     # Get the data from the input and store into variable
        endingLocation = request.form.get('endingLocation')         # Get the data from the input and store into variable
        numOfPassengers = request.form.get('numOfPassenger')        # Get the data from the input and store into variable
        carType = request.form.get('carType')                       # Get the data from the input and store into variable

        if len(startingLocation) < 6 or len(endingLocation) < 6:            # Validation to check if the user input is exactly
            flash("Please enter a valid postal code", category='error')     # 6 digits, if true, continue. Else, return error.
        elif len(endingLocation) > 6 or len(endingLocation) > 6:
            flash("Please enter a valid postal code", category='error')
        else:
            startingCoordinates = mapSearch(startingLocation)           # Get the coordinates of the pickup, based on the postal code, store into a variable
            endingCoordinates = mapSearch(endingLocation)               # Get the coordinates of the drop off, based on the postal code, store into a variable
            origin = (float(startingCoordinates[0]), float(startingCoordinates[1]))     # Store the long and lat of the pickup location
            dest = (float(endingCoordinates[0]), float(endingCoordinates[1]))           # Store the long and lat of the drop-off location
            session["startLocX"] = startingCoordinates[0]   # Store the LONG of pickup into a session
            session["startLocY"] = startingCoordinates[1]   # Store the LAT of pickup into a session
            session["endLocX"] = endingCoordinates[0]       # Store the LONG of drop-off into a session
            session["endLocY"] = endingCoordinates[1]       # Store the LONG of drop-off into a session
            session["startPostal"] = startingLocation       # Store the postal code of starting location into a session
            session["endPostal"] = endingLocation           # Store the postal code of ending location into a session
            session["numOfPassengers"] = numOfPassengers    # Store the number of passengers into a session
            session["carType"] = carType                    # Store the car type into a session
            # Return the distance based on the LONG and LAT of the starting and ending coordinates
            distance = nodeDistance(float(startingCoordinates[0]), float(startingCoordinates[1]), float(endingCoordinates[0]), float(endingCoordinates[1]))
            cost = "{:.2f}".format(distancePricing(distance) * surge())     # Compute the cost based the distance and surge
            session["costPrice"] = cost                                     # Store the cost into a session
            driverLocation = matching_panda(carType, float(numOfPassengers), float(startingCoordinates[0]), float(startingCoordinates[1]))
            if driverLocation[0] is None:
                flash("No driver is found. Please try other options!", category='error')
                return redirect(url_for('views.home'))
            else:
                # Initialise the map, based on the given details
                MapInit(origin, dest, carType, float(numOfPassengers))
                return redirect(url_for('views.routeOutput'))   # Redirect the user to routeOutput HTML
    # Return the values such as current_user, and header title for the HTML to be called
    return render_template("home.html", user=current_user, username=startHeader+username+endHeader)          # Return to home page with current user details


# /rideHistory called by html in base.html
@views.route('/rideHistory', methods=['GET', 'POST'])
@login_required
def rideHistory():
    username = session['username']  # Get the data from the session and store into a variable
    # Return the values such as current_user, and header title for the HTML to be called
    return render_template("rideHistory.html", user=current_user, username=startHeader+username+endHeader)


# /routeOutput called after user enter values to search for driver
@views.route('/routeOutput', methods=['GET', 'POST'])
@login_required
def routeOutput():
    username = session['username']                  # Get the data from the session and store into a variable
    startingLocation = session['startPostal']       # Get the data from the session and store into a variable
    endingLocation = session['endPostal']           # Get the data from the session and store into a variable
    cost = session['costPrice']                     # Get the data from the session and store into a variable
    numOfPassengers = session['numOfPassengers']    # Get the data from the session and store into a variable
    carType = session['carType']                    # Get the data from the session and store into a variable

    if request.method == 'POST':                    # If user click on the submit button in the HTML page
        if request.form['submit_button'] == 'changeRoute':  # If user enter the button to change a route, it enters this if statement
            startingLocation = request.form.get('startingLocation')     # Get the value entered for starting location and store into a variable
            endingLocation = request.form.get('endingLocation')         # Get the value entered for ending location and store into a variable
            if len(startingLocation) < 6 or len(endingLocation) < 6:    # Validate the postal code to ensure it is exactly 6 digit
                flash("Please enter a valid postal code", category='error')
            elif len(endingLocation) > 6 or len(endingLocation) > 6:
                flash("Please enter a valid postal code", category='error')
            else:
                startingCoordinates = mapSearch(startingLocation)       # Return the coordinates based on the postal for pickup
                endingCoordinates = mapSearch(endingLocation)           # Return the coordinates based on the postal for drop-off
                origin = (float(startingCoordinates[0]), float(startingCoordinates[1]))     # Store the LONG and LAT of pickup in a variable
                dest = (float(endingCoordinates[0]), float(endingCoordinates[1]))           # Store the LONG and LAT of drop-off in a variable
                session["startLocX"] = startingCoordinates[0]       # Store the LONG of the pickup location into a session
                session["startLocY"] = startingCoordinates[1]       # Store the LAT of the pickup location into a session
                session["endLocX"] = endingCoordinates[0]           # Store the LONG of the drop-off location into a session
                session["endLocY"] = endingCoordinates[1]           # Store the LAT of the drop-off location into a session
                session["startPostal"] = startingLocation           # Store the postal code of the pickup into a session
                session["endPostal"] = endingLocation               # Store the postal code of the drop-off into a session
                # Calculate the distance based on the LONG and LAT of both pickup and drop-off location
                distance = nodeDistance(float(startingCoordinates[0]), float(startingCoordinates[1]), float(endingCoordinates[0]), float(endingCoordinates[1]))
                # Calculate the cost, based on the distance factor and surge
                cost = "{:.2f}".format(distancePricing(distance) * surge())
                session["costPrice"] = cost     # Store the cost into a session
                # Initialise the map based on the input values
                MapInit(origin, dest, carType, float(numOfPassengers))
                return redirect(url_for('views.routeOutput'))
        elif request.form['submit_button'] == 'confirmRoute':   # If user enter the button to move to confirmation page
            return redirect(url_for('views.confirmationPage'))
    return render_template("routeOutput.html", user=current_user, username=startHeader+username+endHeader, startingPostal=startingLocation, endingPostal=endingLocation, priceCost=cost,
                           numOfPassengers=numOfPassengers, carType=carType)


# /login called by html in base.html
@views.route('/confirmationPage', methods=['GET', 'POST'])
@login_required
def confirmationPage():
    username = session['username']                  # Store the data from the session into the variable
    startingLocation = session['startPostal']       # Store the data from the session into the variable
    endingLocation = session['endPostal']           # Store the data from the session into the variable
    cost = session['costPrice']                     # Store the data from the session into the variable
    numOfPassengers = session['numOfPassengers']    # Store the data from the session into the variable
    carType = session['carType']                    # Store the data from the session into the variable
    startingLocationX = session["startLocX"]
    startingLocationY = session["startLocY"]

    if request.method == 'POST':            # If user click on the submit button
        # Create an object to be added into a row in the transaction order table
        new_transaction = TransactionOrders(pickUpLocation=startingLocation, dropOffLocation=endingLocation, numOfPassengers=numOfPassengers, costPrice=cost, user_id=current_user.id)
        db.session.add(new_transaction)     # Add the object into a session
        db.session.commit()                 # Commit the session
        driverLocation = matching_panda(carType, float(numOfPassengers), float(startingLocationX), float(startingLocationY))
        updateBook(driverLocation)
        return redirect(url_for('views.home'))
    return render_template("confirmationPage.html", user=current_user, username=startHeader+username+endHeader, startingLocation=startingLocation,
                           endingLocation=endingLocation, cost=cost, numOfPassengers=numOfPassengers, carType=carType)


# /login called by html in base.html
@views.route('/helpCentre', methods=['POST', 'GET'])
@login_required
def helpCenter():
    username = session['username']  

    if request.method == 'POST':
        flash("We have received your email. We will reply within 3 working days.", category='success')
        email = request.form.get('email')
        message = request.form.get('message')
        subject = request.form.get('subject')

        msg = Message(subject, sender=email, recipients=['lift.ride.hailing@gmail.com'])
        msg.body = "Email: " + email + "\n\nUsername: " + username + "\n\nMessage: " + message
        mail.send(msg)

        return redirect(url_for('views.home'))

    return render_template("helpCentre.html", user=current_user, username=startHeader+username+endHeader)
   
