import grovepi
import time
import interfaces.grove_rgb_lcd
import interfaces.databaseinterface

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

# this function might need to run for a period of time
def output_RGB(colour, message):   #colour is a tuple of (255,255,255)
    if not ENABLED:
        return -1
    grove_rgb_lcd.setRGB(*colour) 
    grove_rgb_lcd.setText(message)
    return

#only execute the below block if this is the execution point
if __name__ == '__main__':
    interfaces.databaseinterface.set_location = "test.sql"
    results = ViewQuery("SELECT * FROM users")
    print(results)
