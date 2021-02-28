#these imports work relative to the flask app file
from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from grovepiflask.interfaces.grovepiinterface import GrovePiInterface
from datetime import datetime
import time
import globalvars

#STUPID FOLDER STRUCTURE ISNT WORKING - templates folder?????
grovepiblueprint = Blueprint('grovepiblueprint', __name__, template_folder='templates', static_folder='static')

DATABASE = globalvars.DATABASE
GROVEPI = globalvars.DATABASE
LOGGER = globalvars.LOGGER

# homepage for the grovepi
@grovepiblueprint.route('/grovepidashboard', methods=['GET','POST'])
def grovepidashboard():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting da
    enabled = (GROVEPI != None)
    return render_template('grovepidashboard.html', grovepienabled=enabled)

# loads the grovepi
@grovepiblueprint.route('/loadgrovepi', methods=['GET','POST'])
def grovepiload():
    global GROVEPI
    if not GROVEPI:
        GROVEPI = GrovePiInterface(timelimit=20) 
        globalvars.GROVEPI = GROVEPI
        LOGGER.info("loaded grovepi")
    return redirect(url_for('grovepiblueprint.grovepidashboard'))

# shuts down the grove pi
@grovepiblueprint.route('/shutdowngrovepi', methods=['GET','POST'])
def grovepishutdown():
    GROVEPI = None
    LOGGER.info("shutdown grovepi")
    return redirect('/grovepiexample')

@grovepiblueprint.route('/grovepihistory', methods=['GET','POST'])
def grovehistory():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting da
    data = DATABASE.ViewQuery("SELECT * FROM grovehistory")
    return render_template('grovepihistory.html', data=data)

#GET DATA FROM CLIENT - RESIDES ON PYTHON ANYWHERE FLASK SERVER
@grovepiblueprint.route('/handleurlrequest', methods=['GET','POST'])
def handleurlrequest():
    if request.method == "POST":
        hiveid = request.form['hiveid']
        temp = request.form['temp']
        hum = request.form['hum']
        sound = request.form['sound']
        dt = datetime.now()
        DATABASE.ModifyQuery("INSERT INTO grovehistory (hiveid, temp, hum, sound, datetime) VALUES (?,?,?,?,?)",(hiveid, temp, hum, sound, dt))
        message = "Received data from " + str(hiveid)
    return jsonify({"message":message})

@grovepiblueprint.route('/grovepichart', methods=['GET','POST'])
def googlechart():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting da
    enabled = (GROVEPI != None)
    if not GROVEPI:
        flash("You need to load the grove pi!")
        return redirect(url_for('grovepiblueprint.grovepidashboard'))
    return render_template('grovepichart.html', grovepienabled=enabled)


#RASPERRY PI LOCAL WEB SERVER FUNCTIONS------------------------------------#
# use AJAX and JSON to get temperature without a page refresh
# gets the temperature
# homepage for the grovepi

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

#This code is triggered by a recurring AJAX function on client
@grovepiblueprint.route('/getlight', methods=['GET','POST'])
def getlight():
    light = 0
    if GROVEPI:
        if GROVEPI.Configured:
            light = GROVEPI.read_light_sensor_analogueport(2)
    return jsonify({'light':light})

@grovepiblueprint.route('/grovepilcd', methods=['GET','POST'])
def grovepilcd():
    message = request.form['grovelcdmessage']
    if GROVEPI:
        if GROVEPI.Configured:
            colour = (255,0,255)
            GROVEPI.output_RGB(colour,message)
    return jsonify({'message':'rgb activated'})

#------------------------------------------------------------------#
