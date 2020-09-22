from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from interfaces import databaseinterface
from interfaces.grovepiinterface import GrovePiInterface
from datetime import datetime
import time

grovepienabled = False
grovepi = None
grovepiblueprint = Blueprint('grovepiblueprint', __name__, template_folder='templates/grovepi', static_folder='static/grovepi')

# homepage for the grovepi
@grovepiblueprint.route('/grovepiexample', methods=['GET','POST'])
def grovepiexample():
    return render_template('grovepi.html', grovestatus=grovepienabled)

# loads the grovepi
@grovepiblueprint.route('/loadgrovepi', methods=['GET','POST'])
def loadgrovepi():
    globals grovepienabled, grovepi
    grovepi = GrovePiInterface(timelimit=20)
    time.sleep(2)
    grovepienabled = True
    turn_on_led_digitalport(2)
    return jsonify({'message':'Grove Pi enabled'})