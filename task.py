import grovepi
import time
from interfaces import grove_rgb_lcd
from interfaces.databaseinterface import Database
import urlrequest

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

# Read sound sensor
def read_sound_analogueport(port):
    if not ENABLED:
        return -1
    sound = None
    try:
        sound = grovepi.analogRead(port)
    except IOError: #this doesnt appear to work
        print("Error in reading sound sensor")
    return sound

# this function might need to run for a period of time
def output_RGB(colour, message):   #colour is a tuple of (255,255,255)
    if not ENABLED:
        return -1
    grove_rgb_lcd.setRGB(*colour) 
    grove_rgb_lcd.setText(message)
    return

#only execute the below block if this is the execution point
if __name__ == '__main__':
    switch_led_digitalport_value(2)
    sound = read_sound_analogueport(1)
    print("SOUND: " + str(sound))
    [temp,hum] = read_temp_humidity_sensor_digitalport(4)
    time.sleep(0.1) #there is a delay for sensor values
    print("TEMP: " + str(temp))
    print("HUMIDITY: " + str(hum))

    dictofvalues = {"hiveid":1,"temp":temp,"hum":hum,"sound":sound}
    #url = "https://nielbrad.pythonanywhere.com/handleurlrequest"
    url = "http://0.0.0.0:5000/handleurlrequest" #if server is running locally
    response = urlrequest.sendurlrequest(url, dictofvalues)
    print(response)
