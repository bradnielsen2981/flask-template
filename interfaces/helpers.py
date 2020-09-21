import uuid, hashlib, sys, logging, math, time,  socket, os, re 

#---HELPER FUNCTIONS-----------------------------------------------#
sys.tracebacklimit = 1 #Level of python traceback - This works well on Python Anywhere

#Log a variable to the error log or console
def log(message):
    app.logger.info(message)
    return

#for encrypting the password in the database
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

#for decrypting the password in the database - returns True if correct
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

#sender="from@example.com",recipientlist=["to@example.com"])
def send_email(message, sender, recipientlist):
    msg = Message(message,sender,recipientlist)
    mail.send(msg)
    return

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
