import hashlib, socket
import uuid, sys, logging, math, time, os, re
import databaseinterface
from datetime import datetime

logger = logging.getLogger()

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
#get the ip address of the current computer
def get_ip(self):
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

# get the mac address of the current computer
def get_macaddress(self):
    return(':'.join(re.findall('..', '%012x' % uuid.getnode())))

#--DATABASE HELPER FUNCTIONS----------------------------------#
# This has been designed to work with the users table
# updates the users lastaccess in databaseinterface
def update_access(userid):
    fmt = "%d/%m/%Y %H:%M:%S"
    datenow = datetime.now().strftime(fmt)
    databaseinterface.ModifyQuery("UPDATE users SET lastaccess = ?, active = 1 where userid = ?",(datenow, userid))
    return

#--LOGGING HELPERS-----------------#
#Log a message
def log(message):
    logger.info(message)
    return

def log_error(error):
    logger.error(error)
    return

#set the logging
def set_log(log):
    global logger
    logger = log
    return
