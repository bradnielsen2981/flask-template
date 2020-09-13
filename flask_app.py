from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
#from flask_cors import CORS
import sqlite3, uuid, hashlib, sys, logging, math, time #other libraries
from datetime import datetime
from interfaces.databaseinterface import DatabaseHelper

#---SETTINGS for the Flask Web Application
#-----------------------------------------------------------------------------------
DEBUG = True #sets the level of logging to high
SECRET_KEY = 'my random key can be anything' #this random sequence is required to encrypt Sessions
app = Flask(__name__) #Creates a handle for the Flask Web Server
#CORS(app)
app.config.from_object(__name__) #Set app configuration using above SETTINGS
#database = DatabaseHelper('/home/nielbrad/mysite/test.sqlite') #PYTHON ANYWHERE
database = DatabaseHelper('test.sqlite')
database.set_log(app.logger) #set the logger inside the database


#---HTTP REQUEST HANDLERS------------------------------------------------------
#Login page
@app.route('/', methods=['GET','POST'])
def login():
    if 'userid' in session:
        return redirect('./home') #no form data is carried across using 'dot/'
    if request.method == "POST":  #if form data has been sent
        email = request.form['email']   #get the form field with the name 
        password = request.form['password']
        userdetails = database.ViewQueryHelper("SELECT * FROM users WHERE email=? AND password=?",(email,password))
        if userdetails:
            row = userdetails[0] #userdetails is a list of dictionaries
            update_access(row['userid']) #calls my custom helper function
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

#admin page only available to admin, redirects for anyone else
@app.route('/admin', methods=['GET','POST'])
def admin():
    userdetails = database.ViewQueryHelper('SELECT * FROM users')
    if 'permission' in session: #check to see if session cookie contains the permission level
        if session['permission'] != 'admin':
            return redirect('./')
    else:
        return redirect('/') #user has not logged in
    if request.method == 'POST':
        userids = request.form.getlist('delete') #to be used if getting a list of values
        for userid in userids:
            if int(userid) > 1:
                database.ModifyQueryHelper('DELETE FROM users WHERE userid = ?',(int(userid),))
        return redirect('./admin')
    return render_template('admin.html', data=userdetails)

#register a new user - activity for students - create a register page
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        password = request.form['password']
        passwordconfirm = request.form['passwordconfirm']
        if password != passwordconfirm:
            flash("Your passwords do not match")
            return render_template('register.html')
        username = request.form['username']
        #gender = request.form['gender'] 
        #log(gender)
        location = request.form['location']
        email = request.form['email']
        results = database.ViewQueryHelper('SELECT * FROM users WHERE email = ? OR username =?',(email, username))
        if results:
            flash("Your email or username is already in use.")
            return render_template('register.html')
        database.ModifyQueryHelper('INSERT INTO users (username, password, email, location) VALUES (?,?,?,?)',(username, password, email, location))
        return redirect('./')
    return render_template('register.html')

@app.route('/logoff')
def logoff():
    session.clear()
    return redirect('./')









#---ADVANCED EXAMPLES FOR YEAR 12s-------------------------------------#
#Sample Pages
@app.route('/json', methods=['GET','POST'])
def jsontest():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    return render_template('json.html', data=data)

#Bootstrap demo
@app.route('/bootstrap', methods=['GET','POST'])
def bootstrap():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    return render_template('bootstrap.html', data=data)

#Turtle demo
@app.route('/turtle', methods=['GET','POST'])
def turtle():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    if request.method == "POST":
        pass
    return render_template('turtle.html')

#---JSON REQUEST HANDLERS------------------------------------------------#
@app.route('/trighandler', methods=['GET','POST'])
def trighandler():
    c = None
    if request.method == 'POST':
        a = float(request.form.get('sideA'))
        b = float(request.form.get('sideB'))
        c = math.sqrt(a*a + b*b)
    return jsonify({"hypotenuse":c}) #return a python dictionary as JSON - it gets turned into an javascript object in javascript e.g result.hypotenuse 

#json handler is continually called to get a list of the recent users
@app.route('/getactiveusers', methods=['GET','POST'])
def getactiveusers():
    update_access(session['userid']) #calls my custom helper function
    fmt = "%d/%m/%Y %H:%M:%S"
    users = database.ViewQueryHelper("SELECT username, lastaccess from users")
    activeusers = [] #blank list
    for user in users:
        td = datetime.now() - datetime.strptime(user['lastaccess'],fmt)
        if td.seconds < 120:
            activeusers.append(user['username']) #makes a list of names
    return jsonify({'activeusers':activeusers}) #list of users

#---HELPER FUNCTIONS-----------------------------------------------#
#Log a variable to the error log or console
def log(message):
    app.logger.info(message)
    return

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
#------------------------------------------------------------------#

#main method called web server application
if __name__ == '__main__':
    #app.run() #PYTHON ANYTWHERE
    app.run(host='0.0.0.0', port=5000) #runs on port 5000
