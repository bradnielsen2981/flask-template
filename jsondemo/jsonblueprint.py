#these imports work relative to the flask app file
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from datetime import datetime
import helpers
import globalvars

jsonblueprint = Blueprint('jsonblueprint', __name__, template_folder='templates/json', static_folder='static/json')
DATABASE = globalvars.DATABASE

#json test page
@jsonblueprint.route('/json', methods=['GET','POST'])
def jsontest():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    data=None
    return render_template('json.html', data=data)

#calculates the hypotenuse - demonstrates receiving multiple values
@jsonblueprint.route('/trighandler', methods=['GET','POST'])
def trighandler():
    c = None
    if request.method == 'POST':
        a = float(request.form.get('sideA'))
        b = float(request.form.get('sideB'))
        c = helpers.math.sqrt(a*a + b*b)
    return jsonify({"hypotenuse":c}) #return a python dictionary as JSON - it gets turned into an javascript object in javascript e.g result.hypotenuse 

# JSON handler is continually called to get a list of the recent users
@jsonblueprint.route('/getactiveusers', methods=['GET','POST'])
def getactiveusers():
    activeusers = None
    if 'userid' in session:
        helpers.update_access(session['userid']) #calls my custom helper function
    fmt = "%d/%m/%Y %H:%M:%S"
    users = DATABASE.ViewQuery("SELECT username, lastaccess from users")
    activeusers = [] #blank list
    for user in users:
        if user['lastaccess']:
            td = datetime.now() - datetime.strptime(user['lastaccess'],fmt)
            if td.seconds < 120:
                activeusers.append(user['username']) #makes a list of names
    return jsonify({'activeusers':activeusers}) #list of users



