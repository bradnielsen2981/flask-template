from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, Response
from brickpiflask.yourrobot import *
from brickpiflask.interfaces.camerainterface import *
import helpers
from datetime import datetime
import globalvars


brickpiblueprint = Blueprint('brickpiblueprint', __name__, template_folder='templates', static_folder='static')

BRICKPI = globalvars.BRICKPI #ALIAS for globalvars.BRICKPI
DATABASE = globalvars.DATABASE #ALIAS for globalvars.DATABASE

# HTTPS REQUEST HANDERS RETURNING HTML ------------------------------------------
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

#sensor view
@brickpiblueprint.route('/brickpisensorview', methods=['GET','POST'])
def brickpisensorview():
    if 'userid' not in session:
        return redirect('../')
    if not BRICKPI:
        return redirect('../brickpi/brickpidashboard')
    return render_template('brickpisensorview.html', data=BRICKPI.get_all_sensors()) 

# turtle demo
@brickpiblueprint.route('/brickpiturtle', methods=['GET','POST'])
def brickpiturtle():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('../')   #need to use the dot to avoid redirecting data
    if request.method == "POST":
        pass
    return render_template('brickpiturtle.html')


# AJAX REQUEST HANDLERS RETURNING JSON ---------------------
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
            sensorports =  {'thermal':None, 'colour':bp.PORT_1,'ultra':bp.PORT_4,'imu':1 }
            BRICKPI.configure_sensors(motorports,sensorports) #should take 4 secs
            if BRICKPI.Configured:
                sensordict = BRICKPI.get_all_sensors()
    return jsonify({'message':"Brick Pi loaded. Sensor values = " + str(sensordict) })

# AJAX - shutdown the brickpi
@brickpiblueprint.route('/brickpishutdown', methods=['GET','POST'])
def brickpishutdown():
    global BRICKPI #you need to use global if you editing the value of the variable
    if BRICKPI:
        BRICKPI.CurrentRoutine = "stop"
        BRICKPI.safe_exit()
        BRICKPI = None
    return jsonify({'message':'Brick Pi shutting down'})

@brickpiblueprint.route('/brickpiautomate', methods=['GET','POST'])
def brickpiautomate():
    if BRICKPI:
        BRICKPI.automated_search_and_retrieval()
    return jsonify({'message':'Automated searching'})

@brickpiblueprint.route('/brickpistart', methods=['GET','POST'])
def brickpistart():
    data = None
    if BRICKPI:
        data = BRICKPI.move_power_time_until_detect_object(30,4,20,0)
    return jsonify(data)  #python dictionary -> converted JSON

@brickpiblueprint.route('/brickpileft', methods=['GET','POST'])
def brickpileft():
    data = None
    if BRICKPI:
        data = BRICKPI.rotate_power_degrees_IMU_until_detect_object(-30,360,30)
    return jsonify(data)  

@brickpiblueprint.route('/brickpiright', methods=['GET','POST'])
def brickpiright():
    data = None
    if BRICKPI:
        data = BRICKPI.rotate_power_degrees_IMU_until_detect_object(30,360,30)
    return jsonify(data)       

@brickpiblueprint.route('/brickpistop', methods=['GET','POST'])
def brickpistop():
    if BRICKPI:
        BRICKPI.CurrentRoutine = "stop"
        BRICKPI.stop_all()
    return jsonify({'message':'Stopping'})

@brickpiblueprint.route('/brickpishoot', methods=['GET','POST'])
def brickpishoot():
    if BRICKPI:
        BRICKPI.spin_medium_motor(-2000)
    return jsonify({'message':'Shooting'}) 



# CAMERA CODE (Not Sure how it works)
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') #yield is like return

@brickpiblueprint.route('/videofeed')
def videofeed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame') #not actually sure what this code does

