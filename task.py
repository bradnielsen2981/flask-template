import grovepi

ENABLED = True
GROVEPILIGHTSWITCH = False

# Turn on the led using digital port 
def switch_led_digitalport_value(port, value=255):
    if not ENABLED:
        return -1
    global GROVEPILIGHTSWITCH
    grovepi.pinMode(port,"OUTPUT") #should be in initialise
    if GROVEPILIGHTSWITCH:
        grovepi.digitalWrite(port,0)
        GROVEPILIGHTSWITCH = False
    else:
        grovepi.digitalWrite(port,value)
        GROVEPILIGHTSWITCH = True
    return

# Read temp and humidity
def read_temp_humidity_sensor_digitalport(port):
    if not ENABLED:
        return -1
    grovepi.pinMode(tempsensor,"INPUT")
    temp_humidity_list = None
    try:
        temp_humidity_list = grovepi.dht(port,0) #0 - type blue sensor
    except IOError: #this doesnt appear to work
        print("Error in reading the temp and humidity sensor")
    return temp_humidity_list

#turn on the light on digital port 2, 255
switch_led_digitalport_value(2)
print("Temperature and Humidity: " + str(read_temp_humidity_sensor_digitalport(3)))