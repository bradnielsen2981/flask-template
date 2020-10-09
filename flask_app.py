#---PYTHON Libraries for import--------------------------------------
import uuid, sys, logging, math, time, os, re
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g 
from interfaces import databaseinterface
import helpers
from datetime import datetime

#---SETTINGS and GLOBALS----------------------------------#
DEBUG = True #sets the level of logging to high
SECRET_KEY = 'my random key can be anything' #required to encrypt Sessions
app = Flask(__name__) #Creates a handle for the Flask Web Server
app.config.from_object(__name__) #Set app configuration using above SETTINGS
app.config['jsonexamples'] = True
app.config['brickpiexamples'] = False #will only work on Raspberry Pi with BrickPI
app.config['grovepiexamples'] = False #will only work on Raspberry Pi with GrovePi
app.config['emailexamples'] = True
app.config['crossdomainscripting'] = False #allows the server to be accessed from another domain (API)

#--SET LOGGING--------------# log functions are available from helpers.py - import helpers to get logging
helpers.set_log(app.logger) #call helpers.log to log info to console
sys.tracebacklimit = 1 #Level of python traceback - This works well on Python Anywhere to cut down the traceback on errors!!

#---CONDITIONAL IMPORTS AND BLUEPRINTS TO ENABLED ADDITIONAL VIEWS---#
# app.config is a dictionary of global flask variables that can be accessed by html templates
if app.config['jsonexamples']:
    from blueprints.jsonblueprint import jsonblueprint
    app.register_blueprint(jsonblueprint)
if app.config['brickpiexamples']:
    from blueprints.brickpiblueprint import brickpiblueprint
    app.register_blueprint(brickpiblueprint)
if app.config['grovepiexamples']:
    from blueprints.grovepiblueprint import grovepiblueprint
    app.register_blueprint(grovepiblueprint)
if app.config['emailexamples']:
    from interfaces import emailinterface # Needs flask_mail to be installed
    emailinterface.set_mail_server(app) #needs flask_email to be installed
if app.config['crossdomainscripting']:
    from flask_cors import CORS #Needs to be installed, allows cross-domain scripting
    CORS(app) #enables cross domain scripting protection

#--SET UP DATABASE
databaseinterface.set_location('test.sqlite') 
#databaseinterface.set_location('/home/nielbrad/mysite/test.sqlite') #PYTHON ANYWHERE!!!
databaseinterface.set_log(app.logger) #set the logger inside the database

#---HTTP REQUESTS / REQUEST HANDLERS-------------------------------#
#Login page
@app.route('/', methods=['GET','POST'])
def login():
    if 'userid' in session:
        return redirect('./home') #no form data is carried across using 'dot/'
    if request.method == "POST":  #if form data has been sent
        email = request.form['email']   #get the form field with the name 
        password = request.form['password']
        #Activity for students - Hash password to see if it matches database
        userdetails = databaseinterface.ViewQuery("SELECT * FROM users WHERE email=? AND password=?",(email,password))
        if userdetails:
            row = userdetails[0] #userdetails is a list of dictionaries
            helpers.update_access(row['userid']) #calls my custom helper function
            session['userid'] = row['userid']
            session['username'] = row['username']
            session['permission'] = row['permission']
            return redirect('./home')
        else:
            log("Login failed for " + str(email) + " from " + str(get_user_ip()))
            flash("Sorry no user found, password or email incorrect") #flash will send messages to the screen
    return render_template('login.html')

#homepage is shown once user is logged in
@app.route('/home', methods=['GET','POST'])
def home():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    return render_template('home.html', data=data)

# admin page only available to admin - allows admin to update or delete
@app.route('/admin', methods=['GET','POST'])
def admin():
    userdetails = databaseinterface.ViewQuery('SELECT * FROM users')
    if 'permission' in session: #check to see if session cookie contains the permission level
        if session['permission'] != 'admin':
            return redirect('./')
    else:
        return redirect('/') #user has not logged in
    if request.method == 'POST':
        userids = request.form.getlist('delete') #getlist e.g checkboxes
        for userid in userids:
            if int(userid) > 1: #ensure that you can not delete the admin
                databaseinterface.ModifyQuery('DELETE FROM users WHERE userid = ?',(int(userid),)) #a tuple needs atleast 1 comma
        return redirect('./admin')
    return render_template('admin.html', data=userdetails)

# Register a new user - Activity for students - create a register page
# When registering, check if user already exists
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        password = request.form['password']
        passwordconfirm = request.form['passwordconfirm']
        if password != passwordconfirm:
            flash("Your passwords do not match")
            return render_template('register.html')
        username = request.form['username']
        #Activity for students - update database to include a gender field and then modify the INSERT SQL below to include gender
        #gender = request.form['gender'] #not in databaseinterface yet, uses drop down list
        location = request.form['location']
        email = request.form['email']
        results = databaseinterface.ViewQuery('SELECT * FROM users WHERE email = ? OR username =?',(email, username))
        if results:
            flash("Your email or username is already in use.")
            return render_template('register.html')
        #TO DO hash password 
        databaseinterface.ModifyQuery('INSERT INTO users (username, password, email, location) VALUES (?,?,?,?)',(username, password, email, location))
        return redirect('./')
    return render_template('register.html')

# Activity for students
# Update a current user - activity for students - uses GET to pass a value to a URL
# Inside admin page use: <a href="{{ url_for('updateuser',userid=row['userid']) }}">Update</a>
# Create a copy of the registration page called update.html 
# inside input tags use value='{{userdata['email']}}'
@app.route('/updateuser', methods=['GET','POST'])
def updateuser():
    userdata = None
    if request.method == "GET":
        userid = request.values.get('userid')
        #Get the user from the database from userid and send data to registration page
    return render_template('update.html', userdata=userdata)

# log off - clear the session dictionary
@app.route('/logoff')
def logoff():
    session.clear()
    return redirect('./')

# bootstrap demo - Bootstrap is linked to the layout.html page - read W3 schools for more information
@app.route('/bootstrap', methods=['GET','POST'])
def bootstrap():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    return render_template('bootstrap.html', data=data)

#a hard shutdown of the web server - only the admin can shutdown the server
@app.route('/shutdown', methods=['GET','POST'])
def shutdown():
    if 'permission' in session: #check to see if session cookie contains the permission level
        if session['permission'] != 'admin':
            return redirect('./')
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return
#------------------------------------------------------------------#

#main method called web server application
if __name__ == '__main__':
    #app.run() #PYTHON ANYTWHERE!!! will decide the port
    app.run(host='0.0.0.0', port=5000) #runs a local server on port 5000
