#----------------------------------------------------------------------------
# This Database class provides an interface to the database and includes logging
# It's therefore easier to simply inherit the code..
# Created by Brad Nielsen 2019
#--------------------------------------------------------------------
import sqlite3
import sys, logging
from flask import g
from interfaces.databaseinterface import Database

#inherit everything from Database and override connect and disconnect
class FlaskDatabase():

    def __init__(self, location="", log = logging.getLogger(__name__)):
        self.location = location
        self.logger = log
        return

    #set the location
    def set_location(self, l):
        global location
        location = l #location of database file
        return

    # initialise the log
    def set_log(self, log):
        global logger
        logger = log
        return

    # Returns a handle from globals (persistent during request) 
    def connect(self):
        if "db" not in g:
            g.db = sqlite3.connect(self.location)
            g.db.row_factory = sqlite3.Row #configures database queries to return a list of dictionaries (each row/record) [{"field1":value1,"field2":value2...},{etc},{} ]
        return g.db

    # Deletes entry from globals then disconnects
    def disconnect(self):
        db = g.pop("db", None)
        if db is not None:
            db.close()
        return

    # A helper function to save time and also log sql errors
    # Write your Select Query, and pass in a Tuple (a,b,c etc) representing any parameters
    def ViewQuery(self, query, params=None):
        connection = self.connect()
        result = None
        try:
            if params:
                cursor = connection.execute(query, params)
            else:
                cursor = connection.execute(query)
            result = cursor.fetchall() #returns a list of dictionaries
        except (sqlite3.OperationalError, sqlite3.Warning, sqlite3.Error) as e:
            self.logger.error("DATABASE ERROR: %s" % e)
            self.logger.error(query) 
        if result:
            return ([dict(row) for row in result]) #a list of dictionaries
        else:
            return False

    # Created a helper function so to save time and also log results
    # Write your DELETE, INSERT, UPDATE Query, and pass in a Tuple(a,b,c etc ) representing any parameters
    def ModifyQuery(self, query, params=None):
        connection = self.connect()
        result = None
        try:
            if params:
                connection.execute(query, params)
            else:
                connection.execute(query)
            result = True
        except (sqlite3.OperationalError, sqlite3.Warning, sqlite3.Error) as e:
            self.logger.error("DATABASE ERROR: %s" % e)
            self.logger.error(query)
            result = False
        connection.commit()
        return result #Should be a true or false depending on success??

