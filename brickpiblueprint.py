from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, g 
from interfaces import databaseinterface
import helpers
from datetime import datetime

BRICKPIENABLED = False
brickpiblueprint = Blueprint('brickpiblueprint', __name__, template_folder='templates/brickpi', static_folder='static/brickpi')

# homepage for the brickpi
@brickpiblueprint.route('/brickpiexample', methods=['GET','POST'])
def brickpiexample():
    return render_template('brickpi.html', brickpienabled=BRICKPIENABLED)

# load the brickpi
@brickpiblueprint.route('/loadbrickpi', methods=['GET','POST'])
def loadbrickpi():
    BRICKPIENABLED = True
    return jsonify({'message':'robotenabled'})

# turtle demo
@brickpiblueprint.route('/turtle', methods=['GET','POST'])
def turtle():
    if 'userid' not in session: #userid hasnt logged in
        return redirect('./')   #need to use the dot to avoid redirecting data
    if request.method == "POST":
        pass
    return render_template('turtle.html')