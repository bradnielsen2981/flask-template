from datetime import datetime
from flask_mail import Mail, Message 

mailserver = None

def set_mail_server(app):
    global mailserver
    mailserver = Mail(app) #creates the smtp server using the Flask web server
    return

# email script - sender="from@example.com",recipientlist=["to@example.com"])
def send_email(message, sender, recipientlist):
    if MAINSERVER: #You must install flask_mail first and initialise it
        msg = Message(message,sender,recipientlist)
        if mailserver:
            mailserver.send(msg)
    return


