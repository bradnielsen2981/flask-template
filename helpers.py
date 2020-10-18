import hashlib, socket
import uuid, sys, logging, math, time, os, re
from datetime import datetime
import globalvars
import urllib.parse
import urllib.request

#-------------Hashing----------------------------#
#for encrypting the password in the database
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

#for decrypting the password in the database - returns True if correct
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

#------------GENERIC IP Functions-------------------#
#get the ip address of the current server
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# get the ip address of the client who made the request
def get_user_ip():
    return request.remote_addr

# get the mac address of the current computer
def get_macaddress():
    return(':'.join(re.findall('..', '%012x' % uuid.getnode())))

#--LOGGING HELPERS-----------------#
#Log a message
def log(message):
    LOGGER.info(message)
    return

def log_error(error):
    LOGGER.error(error)
    return

#--DATABASE HELPER FUNCTIONS----------------------------------#
# This has been designed to work with the users table
# updates the users lastaccess in databaseinterface
def update_access(userid):
    fmt = "%d/%m/%Y %H:%M:%S"
    datenow = datetime.now().strftime(fmt)
    globalvars.DATABASE.ModifyQuery("UPDATE users SET lastaccess = ?, active = 1 where userid = ?",(datenow, userid))
    return

#---EXTERNAL URL REQUEST LIBRARY---------------------------------------#
def sendurlrequest(url, dictofvalues):
    data = urllib.parse.urlencode(dictofvalues)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)

    #if data is returned
    with urllib.request.urlopen(req) as response:
        responsedata = response.read()
    return responsedata