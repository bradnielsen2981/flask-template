import grovepi
import time

ENABLED = True
grovepilightswitch = False

# Turn on the led using digital port 
def switch_led_digitalport_value(port, value=1):
    if not ENABLED:
        return -1
    global grovepilightswitch
    grovepi.pinMode(port,"OUTPUT") #should be in initialise
    if grovepilightswitch:
        grovepi.digitalWrite(port,0)
        grovepilightswitch = False
    else:
        grovepi.digitalWrite(port,value)
        grovepilightswitch = True
    return

# Read temp and humidity
def read_temp_humidity_sensor_digitalport(port):
    if not ENABLED:
        return -1
    temp_humidity_list = None
    try:
        temp_humidity_list = grovepi.dht(port,0)
    except IOError: #this doesnt appear to work
        print("Error in reading the temp and humidity sensor")
    return temp_humidity_list

print(read_temp_humidity_sensor_digitalport(2))
switch_led_digitalport_value(4,1)
