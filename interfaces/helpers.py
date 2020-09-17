import re, uuid, socket, sys, os

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
