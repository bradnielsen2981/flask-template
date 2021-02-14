from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from brickpiflask.interfaces.brickpiinterface import *
import helpers
from datetime import datetime
import globalvars

brickpiblueprint = Blueprint('brickpiblueprint', __name__, template_folder='templates', static_folder='static')

# homepage for the brickpi
@brickpiblueprint.route('/brickpidashboard', methods=['GET','POST'])
def brickpidashboard():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    enabled = (globalvars.BRICKPI != None)
    return render_template('brickpidashboard.html', robotenabled=enabled) #hides or shows controls

## TO DO: STUDENTS CREATE A SENSOR VIEW USING JSON AND REQUEST
@brickpiblueprint.route('/brickpisensorview', methods=['GET','POST'])
def brickpisensorview():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    if globalvars.BRICKPI == None:
        return redirect('./brickpidashboard')
    return render_template('brickpisensorview.html', sensordata=globalvars.BRICKPI.get_all_sensors()) #hides or shows controls

# AJAX - load the brickpi
@brickpiblueprint.route('/brickpiload', methods=['GET','POST'])
def brickpiload():
    if globalvars.BRICKPI == None:
        globalvars.BRICKPI = load_brickpi(20)
    return jsonify({'message':"Brick Pi loaded"})

# AJAX - shutdown the brickpi
@brickpiblueprint.route('/brickpishutdown', methods=['GET','POST'])
def brickpishutdown():
    globalvars.BRICKPI.safe_exit()
    globalvars.BRICKPI = None
    return jsonify({'message':"Brick Pi shutting down"})

# turtle demo
@brickpiblueprint.route('/brickpiturtle', methods=['GET','POST'])
def brickpiturtle():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    if request.method == "POST":
        pass
    return render_template('brickpiturtle.html')