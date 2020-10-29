#these imports work relative to the flask app file
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from interfaces.grovepiinterface import GrovePiInterface
from datetime import datetime
import time
import globalvars

#STUPID FOLDER STRUCTURE ISNT WORKING - templates folder?????
grovepiblueprint = Blueprint('grovepiblueprint', __name__, template_folder='templates/grovepi', static_folder='static/grovepi')
GROVEPI = globalvars.GROVEPI
DATABASE = globalvars.DATABASE
LOGGER = globalvars.LOGGER

# homepage for the grovepi
@grovepiblueprint.route('/grovepiexample', methods=['GET','POST'])
def grovepiexample():
    enabled = (globalvars.GROVEPI != None)
    return render_template('grovepi.html', grovepienabled=enabled)

# loads the grovepi
@grovepiblueprint.route('/loadgrovepi', methods=['GET','POST'])
def grovepiload():
    if not globalvars.GROVEPI:
        globalvars.GROVEPI = GrovePiInterface(timelimit=20) 
        LOGGER.info("loaded grovepi")
    return redirect('/grovepiexample')

# shuts down the grove pi
@grovepiblueprint.route('/shutdowngrovepi', methods=['GET','POST'])
def grovepishutdown():
    globalvars.GROVEPI = None
    LOGGER.info("shutdown grovepi")
    return redirect('/grovepiexample')

# homepage for the grovepi
@grovepiblueprint.route('/googlechart', methods=['GET','POST'])
def googlechart():
    enabled = (globalvars.GROVEPI != None)
    if not globalvars.GROVEPI:
        flash("You need to load the grove pi!")
        return redirect('/grovepiexample')
    return render_template('googlechart.html', grovepienabled=enabled)

@grovepiblueprint.route('/grovehistory', methods=['GET','POST'])
def grovehistory():
    data = DATABASE.ViewQuery("SELECT * FROM grovehistory")
    return render_template('grovehistory.html', data=data)

#----------------------------------------------------------------------#
# use AJAX and JSON to get temperature without a page refresh
# gets the temperature
@grovepiblueprint.route('/lightswitch', methods=['GET','POST'])
def lightswitch():
    if globalvars.GROVEPI:
        if globalvars.GROVEPI.Configured:
            globalvars.GROVEPI.switch_led_digitalport_value(2,255)
    return jsonify({'message':'Switch light'})

@grovepiblueprint.route('/gettemperaturehumidity', methods=['GET','POST'])
def gettemperaturehumidity():
    if globalvars.GROVEPI:
        if globalvars.GROVEPI.Configured:
            sensorlist = globalvars.GROVEPI.read_temp_humidity_sensor_digitalport(3)
    return jsonify({'temperature':sensorlist[0],'humidity':sensorlist[1]})

#This code is triggered by a recurring AJAX function on client
@grovepiblueprint.route('/getlight', methods=['GET','POST'])
def getlight():
    light = 0
    if globalvars.GROVEPI:
        if globalvars.GROVEPI.Configured:
            light = globalvars.GROVEPI.read_light_sensor_analogueport(2)
    return jsonify({'light':light})