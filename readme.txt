Instructions:

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







