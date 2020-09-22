#----------------------------------------------------------------------------
# This Database class provides an interface to the database and includes logging
# It's therefore easier to simply inherit the code..
# Created by Brad Nielsen 2019
#----------------------------------------------------------------------------
import sqlite3
import logging
import sys
from flask import g #flask has a dictionary of globals for persistent variables between requests.

location = ""
logger = logging.getLogger(__name__)
sys.tracebacklimit = 1 #Level of python traceback - This works well on Python Anywhere

#set the location
def set_location(l):
    global location
    location = l #location of database file
    return

# initialise the log
def set_log(log):
    global logger
    logger = log
    return

# Returns a handle to the Database from globals (persistent during request) 
def connect():
    global location
    if "db" not in g:
        g.db = sqlite3.connect(location)
        g.db.row_factory = sqlite3.Row #configures database queries to return a list of dictionaries (each row/record) [{"field1":value1,"field2":value2...},{etc},{} ]
    return g.db

# Deletes entry from globals
def disconnect():
    db = g.pop("db", None)

    if db is not None:
        db.close()
    return

# A helper function to save time and also log sql errors
# Write your Select Query, and pass in a Tuple (a,b,c etc) representing any parameters
def ViewQuery(query, params=None):
    connection = connect()
    result = None
    try:
        if params:
            cursor = connection.execute(query, params)
        else:
            cursor = connection.execute(query)
        result = cursor.fetchall() #returns a list of dictionaries
    except (sqlite3.OperationalError, sqlite3.Warning, sqlite3.Error) as e:
        logger.error("DATABASE ERROR: %s" % e)
        logger.error(query) 
    disconnect()
    if result:
        return ([dict(row) for row in result]) #change to a list of dictionaries
    else:
        return False

# Created a helper function so to save time and also log results
# Write your DELETE, INSERT, UPDATE Query, and pass in a Tuple(a,b,c etc ) representing any parameters
def ModifyQuery(query, params=None):
    connection = connect()
    result = None
    try:
        if params:
            connection.execute(query, params)
        else:
            connection.execute(query)
        result = True
    except (sqlite3.OperationalError, sqlite3.Warning, sqlite3.Error) as e:
        logger.error("DATABASE ERROR: %s" % e)
        logger.error(query)
        result = False
    connection.commit()
    disconnect()
    return result #Should be a true or false depending on success??

