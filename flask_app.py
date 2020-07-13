from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
import sqlite3, uuid, hashlib, sys, logging #other libraries
from datetime import datetime
from interfaces.databaseinterface import DatabaseHelper

#--------------------------------------------------------------------------------------
# SETTINGS for the Flask Web Application
#-----------------------------------------------------------------------------------
DEBUG = True #sets the level of logging to high
SECRET_KEY = 'my random key can be anything' #this random sequence is required to encrypt Sessions
app = Flask(__name__) #Creates a handle for the Flask Web Server
app.config.from_object(__name__) #Set app configuration using above SETTINGS
#database = DatabaseHelper('/home/nielbrad/mysite/test.sqlite') #on Python Anywhere
database = DatabaseHelper('test.sqlite')
database.set_log(app.logger) #set the logger inside the database

#for encrypting the password in the database
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

#for decrypting the password in the database - returns True if correct
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

#updates the users lastaccess in database
def update_access(userid):
    fmt = "%d/%m/%Y %H:%M:%S"
    datenow = datetime.now().strftime(fmt)
    database.ModifyQueryHelper("UPDATE users SET lastaccess = ?, active = 1 where userid = ?",(datenow, userid))
    return

#gets active users from database using lastaccess field - duration is by default 120 seconds
def get_active_users(duration=120):
    fmt = "%d/%m/%Y %H:%M:%S"
    users = database.ViewQueryHelper("SELECT username, lastaccess from users")
    activeusers = [] #blank list
    for user in users:
        td = datetime.now() - datetime.strptime(user['lastaccess'],fmt)
        if td.seconds < duration:
            activeusers.append(user['name']) #makes a list of names
    return activeusers #list of users as JSON

#HTTP REQUEST HANDLERS------------------------------------------------------
#Login page
@app.route('/', methods=['GET','POST'])
def index():
    if 'userid' in session:
        return redirect('./home') #no form data is carried across using 'dot/'
    if request.method == "POST":  #if form data has been sent
        email = request.form['email']   #get the form field with the name
        password = request.form['password']
        userdetails = database.ViewQueryHelper("SELECT * FROM users WHERE email=? AND password=?",(email,password))
        if userdetails: #list that contains data evaluated to True
            row = userdetails[0] #userdetails is a list of dictionaries, get the first list
            update_access(row['userid'])
            session['userid'] = row['userid']
            session['username'] = row['username']
            session['permission'] = row['permission']
            return redirect('./home')
        else: #an empty list evaluates to False
            log("Incorrect login.")
            flash("Sorry no user found, password or username incorrect")
    else:
        flash("No data submitted")
    return render_template('login.html')


#homepage is shown once user is logged in
@app.route('/home', methods=['GET','POST'])
def home():
    if 'userid' not in session:
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    flash("Login successful")
    return render_template('home.html', data=data)


#admin page only available to admin, redirects for anyone else
@app.route('/admin', methods=['GET','POST'])
def admin():
    data = None
    if 'permission' in session: #check to see if session cookie contains the permission level
        if session['permission'] != 'admin':
            return redirect('./')
    else:
        return redirect('/') #user has not logged in
    if request.method == "POST":
        userids = request.form.getlist('delete') #gets checkboxes, each checkbox contains the user id value
        for userid in userids:
            if int(userid) > 1: #make sure you can not delete the admin user
                database.ModifyQueryHelper("DELETE FROM users WHERE userid = ?",(userid,)) #note the use of comma after userid. A query must accept a list (tuple) of params, not just one param)
    userdetails = database.ViewQueryHelper("SELECT * FROM users")
    return render_template('admin.html', data=userdetails)

#register a new user - activity for students - create a register page
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        pass
        #get all the form fields and store in variables
        #if password does not equal password confirm return an error
        #search database for email, if email is already in use return an error
        #else insert new user into database and redirect to login page
    return render_template('register.html')

@app.route('/logoff')
def logoff():
    session.clear()
    return redirect('./')

#Log a message
def log(message):
    app.logger.info(message)
    return

#----ADVANCED CODING FOR YEAR 12s---------------------------------------
#-------------JSON EXAMPLES---------------------------------------------
@app.route('/defaultdatahandler', methods=['GET','POST'])
def defaultdatahandler():
    var1 = None; var2 = None;
    if request.method == 'POST':
        var1 = request.form.get('var1')
        var2 = request.form.get('var2')
    return jsonify({"returnvar1":var1,"returnvar2":var2})

#example of converting a table of results into JSON
@app.route('/getallusers', methods=['GET','POST'])
def getallusers():
    results = database.ViewQueryHelper("SELECT username, lastaccess from users")
    if results:
        return jsonify([dict(row) for row in results]) #jsonify doesnt work with an SQLite.Row so must convert to list
    else:
        return jsonify({"message":"No users found"}) #jsonigy converts a python dictionary to string encoding
#-------------------------------------------------------------------------------------------


#main method called web server application
if __name__ == '__main__':
    #app.run() #on python anywhere you will be able to access your server through your web app link
    app.run(host='0.0.0.0', port=5000) #runs on port 5000
