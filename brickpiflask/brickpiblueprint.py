from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from brickpiflask.yourrobot import *
import helpers
from datetime import datetime
import globalvars


brickpiblueprint = Blueprint('brickpiblueprint', __name__, template_folder='templates', static_folder='static')

BRICKPI = globalvars.BRICKPI #ALIAS for globalvars.BRICKPI
DATABASE = globalvars.DATABASE #ALIAS for globalvars.DATABASE

# homepage for the brickpi
@brickpiblueprint.route('/', methods=['GET','POST'])
def brickpihome():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting da
    return render_template('brickpihome.html') 

# dashboard for the brickpi
@brickpiblueprint.route('/brickpidashboard', methods=['GET','POST'])
def brickpidashboard():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting da
    enabled = (BRICKPI != None)
    return render_template('brickpidashboard.html', robotenabled=enabled) #hides or shows controls

## TO DO: STUDENTS CREATE A SENSOR VIEW USING JSON AND REQUEST
@brickpiblueprint.route('/brickpisensorview', methods=['GET','POST'])
def brickpisensorview():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting data
    if BRICKPI == None:
        flash("Brick PI is not yet loaded!!")
        return redirect(url_for('brickpiblueprint.brickpidashboard'))
    return render_template('brickpisensorview.html', data=BRICKPI.get_all_sensors()) 

# turtle demo
@brickpiblueprint.route('/brickpiturtle', methods=['GET','POST'])
def brickpiturtle():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting data
    if request.method == "POST":
        pass
    return render_template('brickpiturtle.html')




# ----------AJAX / JSON REQUEST HANDLERS ---------------------------------
# AJAX - load the brickpi
@brickpiblueprint.route('/brickpiload', methods=['GET','POST'])
def brickpiload():
    global BRICKPI
    if BRICKPI == None:
        BRICKPI = load_robot(20, globalvars.LOGGER)
        globalvars.BRICKPI = BRICKPI #update reference in global
        sensordict = "Not Loaded"
        if BRICKPI:
            bp = BRICKPI.BP #alias to shorten code
            motorports = {'rightmotor':bp.PORT_B, 'leftmotor':bp.PORT_C, 'mediummotor':bp.PORT_D }
            sensorports =  { 'thermal':bp.PORT_2, 'colour':bp.PORT_1,'ultra':bp.PORT_4,'imu':1 }
            BRICKPI.configure_sensors(motorports,sensorports) #should take 4 secs
            if BRICKPI.Configured:
                sensordict = BRICKPI.get_all_sensors()
    return jsonify({'message':"Brick Pi loaded. Sensor values = " + str(sensordict) })

# AJAX - shutdown the brickpi
@brickpiblueprint.route('/brickpishutdown', methods=['GET','POST'])
def brickpishutdown():
    global BRICKPI #you need to use global if you editing the value of the variable
    if BRICKPI:
        BRICKPI.safe_exit()
        BRICKPI = None
    return jsonify({'message':"Brick Pi shutting down"})

# start the robot
@brickpiblueprint.route('/brickpistart', methods=['GET','POST'])
def brickpistart():
    if BRICKPI:
        BRICKPI.move_power(-30, 3)
    return jsonify({'message':"start"})

# stop the robot
@brickpiblueprint.route('/brickpistop', methods=['GET','POST'])
def brickpistop():
    if BRICKPI:
        BRICKPI.stop_all()
    return jsonify({'message':"Robot is stopping"})

# start the robot
@brickpiblueprint.route('/brickpileft', methods=['GET','POST'])
def brickpileft():
    if BRICKPI:
        BRICKPI.rotate_power(-30)
    return jsonify({'message':"Robot turning left"})

# stop the robot
@brickpiblueprint.route('/brickpiright', methods=['GET','POST'])
def brickpiright():
    if BRICKPI:
        BRICKPI.rotate_power(30)
    return jsonify({'message':"Robot turning right"})

# stop the robot
@brickpiblueprint.route('/brickpishoot', methods=['GET','POST'])
def brickpishoot():
    if BRICKPI:
        BRICKPI.spin_medium_motor(2000)
    return jsonify({'message':"Fire"})

@brickpiblueprint.route('/brickpirotatedegrees', methods=['GET','POST'])
def brickpirotatedegrees():
    if BRICKPI:
        BRICKPI.rotate_power_degrees_IMU(30, 90)
    return jsonify({'message':"rotate 90 degrees"})

@brickpiblueprint.route('/brickpirotateheading', methods=['GET','POST'])
def brickpirotateheading():
    if BRICKPI:
        BRICKPI.rotate_power_heading_IMU(30, 90)
    return jsonify({'message':"rotate heading"})

@brickpiblueprint.route('/brickpimove', methods=['GET','POST'])
def brickpimove():
    if BRICKPI:
        BRICKPI.move_power_time(30, 3)
    return jsonify({'message':"move time"})


