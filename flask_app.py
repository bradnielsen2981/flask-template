#---PYTHON Libraries for import--------------------------------------
import uuid, sys, logging, math, time, os, re
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g 
#from flask_cors import CORS #Needs to be installed, allows cross-domain scripting
from brickpiblueprint import brickpiblueprint
from grovepiblueprint import grovepiblueprint
from jsonblueprint import jsonblueprint
from interfaces import databaseinterface, helpers
#from interfaces import emailinterface # Needs flask_mail to be installed 
from datetime import datetime

#---SETTINGS and GLOBALS----------------------------------#
DEBUG = True #sets the level of logging to high
SECRET_KEY = 'my random key can be anything' #required to encrypt Sessions
app = Flask(__name__) #Creates a handle for the Flask Web Server
app.register_blueprint(brickpiblueprint) #brickpi library needs to be installed
app.register_blueprint(grovepiblueprint) #grove library needs to be installed
app.register_blueprint(jsonblueprint)
app.config.from_object(__name__) #Set app configuration using above SETTINGS
#CORS(app) #enables cross domain scripting protection
#helpers.set_mail_server(app) #flask_mail needs to be installed
databaseinterface.set_location('test.sqlite')
#databaseinterface.set_location('/home/nielbrad/mysite/test.sqlite') #PYTHON ANYWHERE
databaseinterface.set_log(app.logger) #set the logger inside the database
helpers.set_log(app.logger) #call helpers.log to log info to console
sys.tracebacklimit = 1 #Level of python traceback - This works well on Python Anywhere

#---HTTP REQUESTS / RESPONSES HANDLERS-------------------------------#
#Login page
@app.route('/', methods=['GET','POST'])
def login():
    if 'userid' in session:
        return redirect('./home') #no form data is carried across using 'dot/'
    if request.method == "POST":  #if form data has been sent
        email = request.form['email']   #get the form field with the name 
        password = request.form['password']
        #TO DO - Hash password to see if it matches database
        userdetails = databaseinterface.ViewQuery("SELECT * FROM users WHERE email=? AND password=?",(email,password))
        if userdetails:
            row = userdetails[0] #userdetails is a list of dictionaries
            helpers.update_access(row['userid']) #calls my custom helper function
            session['userid'] = row['userid']
            session['username'] = row['username']
            session['permission'] = row['permission']
            return redirect('./home')
        else:
            flash("Sorry no user found, password or email incorrect")
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
            if int(userid) > 1:
                databaseinterface.ModifyQuery('DELETE FROM users WHERE userid = ?',(int(userid),))
        return redirect('./admin')
    return render_template('admin.html', data=userdetails)

# register a new user - Activity for students - create a register page
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
# update a current user - activity for students - uses GET to pass a value to a URL
# inside admin page use <a href="{{ url_for('updateuser',userid=row['userid']) }}">Update</a> to allow update of each user
@app.route('/updateuser', methods=['GET','POST'])
def updateuser():
    if request.method == "GET":
        userid = request.values.get('userid')
        #Get the user based on userid and send data to registration page
    return render_template('register.html')

# log off - clear the session dictionary
@app.route('/logoff')
def logoff():
    session.clear()
    return redirect('./')

# bootstrap demo
@app.route('/bootstrap', methods=['GET','POST'])
def bootstrap():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    return render_template('bootstrap.html', data=data)
#------------------------------------------------------------------#

#main method called web server application
if __name__ == '__main__':
    #app.run() #PYTHON ANYTWHERE
    app.run(host='0.0.0.0', port=5000) #runs a local server on port 5000
