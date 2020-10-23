#---PYTHON LIBRARIES FOR IMPORT--------------------------------------
import uuid, sys, logging, math, time, os, re
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from interfaces.databaseinterface import Database
from datetime import datetime
import globalvars

#---CONFIGURE APP---------------------------------------------------#
sys.tracebacklimit = 1 #Level of python traceback - useful for reducing error text
app = Flask(__name__) #Creates the Flask Server Object
#from flask import current_app as app can be used to access any of these variables
app.config.from_object('config.Config')
globalvars.LOGGER = app.logger; LOGGER = globalvars.LOGGER
globalvars.DATABASE = Database('test.sqlite', app.logger); DATABASE = globalvars.DATABASE
#/home/nielbrad/mysite/test.sqlite
#app.config['DATABASE'] = FlaskDatabase('/home/nielbrad/mysite/test.sqlite') #PYTHON ANYWHERE!

if app.config['JSON']:
    from blueprints.jsonblueprint import jsonblueprint
    app.register_blueprint(jsonblueprint)
if app.config['BRICKPI']:
    from blueprints.brickpiblueprint import brickpiblueprint
    app.register_blueprint(brickpiblueprint)
if app.config['GROVEPI']:
    from blueprints.grovepiblueprint import grovepiblueprint
    app.register_blueprint(grovepiblueprint)
if app.config['EMAIL']:
    from interfaces import emailinterface # Needs flask_mail to be installed
    emailinterface.set_mail_server(app) #needs flask_email to be installed
if app.config['CROSSDOMAIN']:
    from flask_cors import CORS #Needs to be installed, allows cross-domain scripting
    CORS(app) #enables cross domain scripting protection

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
        userdetails = DATABASE.ViewQuery("SELECT * FROM users WHERE email=? AND password=?",(email,password))
        if userdetails:
            row = userdetails[0] #userdetails is a list of dictionaries
            update_access(row['userid']) #calls my custom helper function
            session['userid'] = row['userid']
            session['username'] = row['username']
            session['permission'] = row['permission']
            return redirect('./home')
        else:
            LOGGER.error("Login failed for " + str(email) + " from " + str(get_user_ip()))
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
    userdetails = DATABASE.ViewQuery('SELECT * FROM users')
    if 'permission' in session: #check to see if session cookie contains the permission level
        if session['permission'] != 'admin':
            return redirect('./')
    else:
        return redirect('/') #user has not logged in
    if request.method == 'POST':
        userids = request.form.getlist('delete') #getlist e.g checkboxes
        for userid in userids:
            if int(userid) > 1: #ensure that you can not delete the admin
                DATABASE.ModifyQuery('DELETE FROM users WHERE userid = ?',(int(userid),)) #a tuple needs atleast 1 comma
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
        results = DATABASE.ViewQuery('SELECT * FROM users WHERE email = ? OR username =?',(email, username))
        if results:
            flash("Your email or username is already in use.")
            return render_template('register.html')
        #TO DO hash password 
        DATABASE.ModifyQuery('INSERT INTO users (username, password, email, location) VALUES (?,?,?,?)',(username, password, email, location))
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

# update access
def update_access(userid):
    fmt = "%d/%m/%Y %H:%M:%S"
    datenow = datetime.now().strftime(fmt)
    DATABASE.ModifyQuery("UPDATE users SET lastaccess = ?, active = 1 where userid = ?",(datenow, userid))
    return
#------------------------------------------------------------------#


@app.route('/grovehistory', methods=['GET','POST'])
def grovehistory():
    data = DATABASE.ViewQuery("SELECT * FROM grovehistory")
    return render_template('grovehistory.html', data=data)

#GET DATA FROM CLIENT - RESIDES ON PYTHON ANYWHERE FLASK SERVER
@app.route('/handleurlrequest', methods=['GET','POST'])
def handleurlrequest():
    if request.method == "POST":
        hiveid = request.form['hiveid']
        temp = request.form['temp']
        hum = request.form['hum']
        sound = request.form['sound']
        dt = datetime.now()
        DATABASE.ModifyQuery("INSERT INTO grovehistory (hiveid, temp, hum, sound, datetime) VALUES (?,?,?,?,?)",(hiveid, temp, hum, sound, dt))
        message = "Received data from " + str(hiveid)
        LOGGER.info(message)
    return jsonify({"message":message})

#main method called web server application
if __name__ == '__main__':
    #app.run() #PYTHON ANYTWHERE!!! will decide the port
    app.run(host='0.0.0.0', port=5000) #runs a local server on port 5000
