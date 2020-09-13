import re
import uuid
import socket
import sys
import os
from smtplib import *
from smtplib import SMTP # use this for standard SMTP protocol (port 25, no encryption)
from email.MIMEText import MIMEText

#get the ip address
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

# get the mac address of the device
def get_macaddress(self):
    return(':'.join(re.findall('..', '%012x' % uuid.getnode())))

SMTPserver = 'smtp.live.com' # This is the SMTP server. In our example, we use Microsoft Outlook.
sender =     'dex@outlook.com' # This is your login email.
destination = ['dex@dexterindustries.com'] # This is the e-mail 
USERNAME = "dex@outlook.com"
PASSWORD = "my_password"
# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'
content="""\Test message"""

def send_email(content, destination, subject):
    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all
        # timeout is critical here for long term health.  
        conn = SMTP(SMTPserver, port = 587, timeout = 60)
        conn.ehlo()
        conn.starttls()
        conn.ehlo()
        conn.login(USERNAME, PASSWORD)
        conn.set_debuglevel(1)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.close()

    except Exception as exc:
        # sys.exit( "mail failed; %s" % str(exc) ) # give a error message
        print("Mail failed; %s" % str(exc))
        print("Moving on!")