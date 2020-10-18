from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g
from flask import current_app as app #imports globals
from interfaces.brickpiinterface import *
import helpers
from datetime import datetime
import globalvars

brickpiblueprint = Blueprint('brickpiblueprint', __name__, template_folder='templates/brickpi', static_folder='static/brickpi')
GROVEPI = globalvars.BRICKPI
DATABASE = globalvars.DATABASE

# homepage for the brickpi
@brickpiblueprint.route('/brickpiexample', methods=['GET','POST'])
def brickpiexample():
    enabled = (BRICKPI != None)
    return render_template('brickpi.html', brickpienabled=enabled)

# load the brickpi
@brickpiblueprint.route('/loadbrickpi', methods=['GET','POST'])
def loadbrickpi():
    if not BRICKPI:
        load_brickpi()
    return redirect('/brickpiexample')

# shutdown the brickpi
@brickpiblueprint.route('/shutdownbrickpi', methods=['GET','POST'])
def shutdownbrickpi():
    BRICKPI = None
    return redirect('/brickpiexample')

# turtle demo
@brickpiblueprint.route('/turtle', methods=['GET','POST'])
def turtle():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    if request.method == "POST":
        pass
    return render_template('turtle.html')