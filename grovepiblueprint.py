from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from interfaces import databaseinterface
from interfaces import grovepiinterface
from datetime import datetime
import helpers
import time

grovepi = None #grove object
grovepiblueprint = Blueprint('grovepiblueprint', __name__, template_folder='templates/grovepi', static_folder='static/grovepi')

# homepage for the grovepi
@grovepiblueprint.route('/grovepiexample', methods=['GET','POST'])
def grovepiexample():
    return render_template('grovepi.html', grovestatus=grovepienabled)

# loads the grovepi
@grovepiblueprint.route('/loadgrovepi', methods=['GET','POST'])
def loadgrovepi():
    global grovepi
    if not grovepi:
        grovepi = grovepiinterface.GrovePiInterface(timelimit=20)
        grovepi.turn_on_led_digitalport(2)
        time.sleep(2)
        helpers.log("loaded grovepi")
    return jsonify({'message':'Grove Pi enabled'})

@grovepiblueprint.route('/gettemperature', methods=['GET','POST'])
def gettemperature():
    if grovepiinterface.ENABLED:
        temperaturelist = grovepi.read_temp_humidity_sensor_digitalport(3)
    return jsonify({'temperature':temperaturelist})

