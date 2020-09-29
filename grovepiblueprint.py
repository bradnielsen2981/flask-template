from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from interfaces import databaseinterface
from interfaces import grovepiinterface
from datetime import datetime
import helpers
import time

grovepi = None #grove object
grovepienabled = False
grovepiblueprint = Blueprint('grovepiblueprint', __name__, template_folder='templates/grovepi', static_folder='static/grovepi')

# homepage for the grovepi
@grovepiblueprint.route('/grovepiexample', methods=['GET','POST'])
def grovepiexample():
    return render_template('grovepi.html', grovepienabled=grovepienabled)

# loads the grovepi
@grovepiblueprint.route('/loadgrovepi', methods=['GET','POST'])
def grovepiload():
    global grovepi, grovepienabled
    grovepienabled = True
    if not grovepi:
        grovepi = grovepiinterface.GrovePiInterface(timelimit=20)
        grovepi.set_log(helpers.logger)
        helpers.log("loaded grovepi")
    return redirect('/grovepiexample')

# shuts down the grove pi
@grovepiblueprint.route('/shutdowngrovepi', methods=['GET','POST'])
def grovepishutdown():
    global grovepi, grovepienabled
    grovepienabled = False
    helpers.log("shutdown grovepi")
    return redirect('/grovepiexample')

# homepage for the grovepi
@grovepiblueprint.route('/googlechart', methods=['GET','POST'])
def googlechart():
    if not grovepienabled:
        flash("You need to load the grove pi!")
        return redirect('/grovepiexample')
    return render_template('googlechart.html', grovepienabled=grovepienabled)

#----------------------------------------------------------------------------#
# use AJAX and JSON to get temperature without a page refresh
# gets the temperature
@grovepiblueprint.route('/lightswitch', methods=['GET','POST'])
def lightswitch():
    if grovepiinterface.ENABLED:
        grovepi.switch_led_digitalport_value(2,255)
    return jsonify({'message':'Switch light'})

@grovepiblueprint.route('/gettemperaturehumidity', methods=['GET','POST'])
def gettemperaturehumidity():
    if grovepiinterface.ENABLED:
        sensorlist = grovepi.read_temp_humidity_sensor_digitalport(3)
        return jsonify({'temperature':sensorlist[0],'humidity':sensorlist[1]})
    return jsonify({'message':'GrovePi Not Enabled'})

@grovepiblueprint.route('/getlight', methods=['GET','POST'])
def getlight():
    light = 0
    if grovepiinterface.ENABLED:
        light = grovepi.read_light_sensor_analogueport(2)
    return jsonify({'light':light})