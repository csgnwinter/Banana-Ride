# README

## 1. Overview
This is a ride hailing app, Banana Ride. The main features are generating the shortest route from start to end point and matching the users with the nearest available driver according to user pereferences. Other features include Account Creation, Help Centre and Ride History. This implementation is limited to the area of Jurong West, Singapore due to limited resources and small assigned time frame. 

## 2. Features
   ### *Account Creation*
Users can create an account if they haven't yet to begin using the application. All accounts are stored in an SQL database
    

https://user-images.githubusercontent.com/93068145/164891978-a3133dae-e005-45cc-9f60-2f8a96f5cace.mov


    
   ### *A-Star Search Algorithm*
User enters 2 postal codes for their start and end locations along with their preferred seats and car type. The algorithm then calculates the shortest route between these two points by using the A* Search algorithm and generates a map with the route plotted. Route plotted is shown by a black line and the start and end points are represented by a yellow pin.
    

https://user-images.githubusercontent.com/93068145/164891985-63842269-d82f-4368-8da0-c7f66909b4f6.mov


   ### *Driver Matching*
A nearest available driver, based on user's preference of seats and car type, is then matched to user if there is any. The matched driver's location is then shown on the generated map on the second page. The driver's location is marked with a banana car.

<img width="1126" alt="Screenshot 2022-04-23 at 7 09 31 PM" src="https://user-images.githubusercontent.com/93068145/164892026-80f8bea2-fb43-4421-a848-ed59427fade1.png">

   ### *Changing locations*
While on the second preview page, users have the option to re-enter their start and end locations if they change their minds. Once they click confirm to change the points, the map on the page is then updated with the appropriate and accurate representation of route and the nearest driver matched.
    

https://user-images.githubusercontent.com/93068145/164891990-a72f99d4-6584-4f9e-beed-d6e61f833ae3.mov


   ### *Ride History*
Users are able to see their ride history with all necessary information should they wish to keep track of their travelling and expenses.
    

https://user-images.githubusercontent.com/93068145/164891998-3d41152c-6d4d-4f01-bb25-d2e553438d60.mov


   ### *Help Center*
Users have access to a help center where they can send an email to the help center for any enquiries they may have.
    
    

https://user-images.githubusercontent.com/93068145/164891995-5f5a40f4-1268-461a-b222-48406987f6d7.mov


## 3. Installation Guide:

1. To be able to run our code you would first need to install anaconda if you haven't already
2. Once you have anaconda installed, run the following lines of code in your Command Prompt/Terminal 
    a. conda config --prepend channels conda-forge
    b. conda create -n ox --yes python=3.9.12 osmnx 
    c. conda activate ox
3. Step 2 should have created a new conda environment named ox with osmnx installed 
4. To confirm, open the anaconda navigator app click on the Environments tab on the left and check whether there is a new environment named "ox"
5. Now you will need to install the remaining necessary modules to run this project
5. Select on the newly created environment, "ox", and on the right side of your application you will see a list of modules
6. Select "All" from the drop down menu beside the "Channels" button
7. Now you will want to search for the following modules and check/select them 
    a. (flask, flask-login, flask-sqlalchemy, flask-mail, networkx, folium, pandas)
8. Upon selection click Apply then click Apply again
9. Now go back to the Home tab and open VSCode(or whichever IDE you are using) using the anaconda navigator
10. Once finished open your IDE of choice and change the interpreter to the newly created conda environment
    a. For VSCode press ctrl-shift-P and search "Python: Select interpreter" then select the newly created conda (ox)
11. Finally run the first_time_run.py file to generate our map in graphml format, once done you are ready to run the website by running the main.py
12. If you are unable to run the main.py or it is taking quite long to return the IP of the website you might need to add the anaconda file path(/anaconda) as on of your environment variables as well as (/anaconda/Library/bin) and (/anaconda/Scripts))
11. Website IP will be 127.0.0.1







