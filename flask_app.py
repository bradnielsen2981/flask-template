from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
import sqlite3, uuid, hashlib, sys, logging #other libraries
from datetime import datetime
from databaseinterface import DatabaseHelper

#--------------------------------------------------------------------------------------
# SETTINGS for the Flask Web Application
#-----------------------------------------------------------------------------------
DEBUG = True #sets the level of logging
SECRET_KEY = 'my random key can be anything' #this random sequence is required to encrypt Sessions
app = Flask(__name__) #Creates a handle for the Flask Web Server
app.config.from_object(__name__) #Set app configuration using above SETTINGS
database = DatabaseHelper('/home/nielbrad/mysite/test.sqlite')

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

#gets active users from database using lastaccess field
def get_active_users():
    fmt = "%d/%m/%Y %H:%M:%S"
    users = database.ViewQueryHelper("SELECT username, lastaccess from users")
    activeusers = [] #blank list
    for user in users:
        td = datetime.now() - datetime.strptime(user['lastaccess'],fmt)
        if td.seconds < 120:
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

@app.route('/register', methods=['GET','POST'])
def register():
    data = None
    if request.method == "POST":
        name = request.form['name']   #get the form field with the name username
        password = request.form['password']
        passwordconfirm = request.form['passwordconfirm']
        phone = request.form['phone']
        age = request.form['age']
        email = request.form['email']
        if password != passwordconfirm:
            flash("Passwords do no match!") #flash is a means of debugging on the web page before and after redirects
            return render_template('register.html', data=data) #exit function
        users = database.ViewQueryHelper("SELECT * FROM users WHERE email = ?",(email,)) #check that the username doesnt already exist
        if (users != None):
            flash("Username already exists!")
            return render_template('register.html', data=data) #exit function
        database.ModifyQueryHelper("INSERT INTO users (name, password, permission, email, phone, active) VALUES (?,?,?,?,?,?)",(name,password,'user',email,phone,1))
        return redirect('./')
    return render_template('register.html', data=data)

@app.route('/home', methods=['GET','POST'])
def home():
    if 'userid' not in session:
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    flash("Login successful")
    return render_template('home.html', data=data)

@app.route('/admin', methods=['GET','POST'])
def admin():
    data = None
    if 'permission' in session:
        if session['permission'] != 'admin':
            return redirect('./')
    else:
        return redirect('/')
    if request.method == "POST":
        userids = request.form.getlist('delete')
        for userid in userids:
            if int(userid) > 1: #make sure you can not delete the admin user
                database.ModifyQueryHelper("DELETE FROM users WHERE userid = ?",(userid,))
    userdetails = database.ViewQueryHelper("SELECT * FROM users")
    return render_template('admin.html', data=userdetails)

#-------------JSON EXAMPLES------------------------------------
@app.route('/defaultdatahandler', methods=['GET','POST'])
def defaultdatahandler():
    if request.method == 'POST':
        var1 = request.form.get('var1')
        var2 = request.form.get('var2')
    return jsonify({"returnvar1":"value1","returnvar2":"value2"})

#example of converting a table of results into JSON
@app.route('/getallusers', methods=['GET','POST'])
def getallusers():
    results = database.ViewQueryHelper("SELECT username, lastaccess from users")
    return jsonify([dict(row) for row in results]) #jsonify doesnt work with an SQLite.Row so must convert
#-------------------------------------------------------------------------------------------

@app.route('/logoff')
def logoff():
    session.clear()
    return redirect('./')

#Log a message
def log(message):
    app.logger.info(message)
    return

#main method called web server application
if __name__ == '__main__':
    app.run()