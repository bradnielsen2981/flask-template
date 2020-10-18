#these imports work relative to the flask app file
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from interfaces.grovepiinterface import GrovePiInterface
from datetime import datetime
import time
import globalvars

grovepiblueprint = Blueprint('grovepiblueprint', __name__, template_folder='templates/grovepi', static_folder='static/grovepi')
GROVEPI = globalvars.GROVEPI
DATABASE = globalvars.DATABASE

# homepage for the grovepi
@grovepiblueprint.route('/grovepiexample', methods=['GET','POST'])
def grovepiexample():
    enabled = (GROVEPI != None)
    DATABASE.ViewQuery("SELECT * FROM users")
    return render_template('grovepi.html', grovepienabled=enabled)

# loads the grovepi
@grovepiblueprint.route('/loadgrovepi', methods=['GET','POST'])
def grovepiload():
    if not GROVEPI:
        GROVEPI = GrovePiInterface(timelimit=20) 
        LOGGING.info("loaded grovepi")
    return redirect('/grovepiexample')

# shuts down the grove pi
@grovepiblueprint.route('/shutdowngrovepi', methods=['GET','POST'])
def grovepishutdown():
    GROVEPI = None
    LOGGING.info("shutdown grovepi")
    return redirect('/grovepiexample')

# homepage for the grovepi
@grovepiblueprint.route('/googlechart', methods=['GET','POST'])
def googlechart():
    enabled = (GROVEPI != None)
    if not GROVEPI:
        flash("You need to load the grove pi!")
        return redirect('/grovepiexample')
    return render_template('googlechart.html', grovepienabled=enabled)

#----------------------------------------------------------------------#
# use AJAX and JSON to get temperature without a page refresh
# gets the temperature
@grovepiblueprint.route('/lightswitch', methods=['GET','POST'])
def lightswitch():
    if GROVEPI:
        if GROVEPI.Configured:
            GROVEPI.switch_led_digitalport_value(2,255)
    return jsonify({'message':'Switch light'})

@grovepiblueprint.route('/gettemperaturehumidity', methods=['GET','POST'])
def gettemperaturehumidity():
    if GROVEPI:
        if GROVEPI.Configured:
            sensorlist = GROVEPI.read_temp_humidity_sensor_digitalport(3)
    return jsonify({'temperature':sensorlist[0],'humidity':sensorlist[1]})

@grovepiblueprint.route('/getlight', methods=['GET','POST'])
def getlight():
    light = 0
    if GROVEPI:
        if GROVEPI.Configured:
            light = GROVEPI.read_light_sensor_analogueport(2)
    return jsonify({'light':light})