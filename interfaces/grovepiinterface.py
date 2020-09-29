import grovepi
import time, math, sys, logging, threading
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease 
from di_sensors.temp_hum_press import TempHumPress
import grove_rgb_lcd
#from interfaces import helpers  #when run as a blueprint the import needs to change
import helpers

ENABLED = False
grovepilightswitch = False

class GrovePiInterface():

    #Initialise log and timelimit (used to exit a function after time)
    def __init__(self, timelimit=20):
        global ENABLED
        self.timelimit = timelimit
        self.CurrentCommand = "loading"
        self.Configured = False #is the grove configured?
        ENABLED = True
        return

    # This function will return the current light reading from the desired ANALOG port A0
    def read_light_sensor_analogueport(self, port):
        light_sensor = port
        grovepi.pinMode(light_sensor,"INPUT")
        sensor_value = None
        try:
            sensor_value = grovepi.analogRead(light_sensor) # Get sensor value
        except IOError: #this doesnt appear to work
            helpers.log_error("Error in reading the light sensor")
        return sensor_value

    # This function will return the current ultra sonic from the digital port
    def read_ultra_digitalport(self, port):
        ultra = port
        grovepi.pinMode(ultra,"INPUT")
        sensor_value = None
        try:
            sensor_value = grovepi.ultrasonicRead(ultra) # Get sensor value
        except IOError: #this doesnt appear to work
            helpers.log_error("Error in reading the ultra sensor")
        return sensor_value

    #Turn on the led using digital port 
    def switch_led_digitalport_value(self, port, value):
        global grovepilightswitch
        grovepi.pinMode(port,"OUTPUT") #should be in initialise
        if grovepilightswitch:
            grovepi.digitalWrite(port,0)
            grovepilightswitch = False
        else:
            grovepi.digitalWrite(port,value)
            grovepilightswitch = True
        return

    #read temp and humidity
    def read_temp_humidity_sensor_digitalport(self, port):
        tempsensor = port
        grovepi.pinMode(tempsensor,"INPUT")
        temp_humidity_list = None
        try:
            temp_humidity_list = grovepi.dht(port,0) #0 - type blue sensor
        except IOError: #this doesnt appear to work
            helpers.log_error("Error in reading the temp and humidity sensor")
        return temp_humidity_list

    #get the current moisture
    def read_moisture_sensor_analogueport(self, port):
        moisture_sensor = port
        grovepi.pinMode(moisture_sensor,"INPUT")
        moisture = None
        try:
            moisture = grovepi.analogRead(moisture_sensor)
        except IOError: #this doesnt appear to work
            helpers.log_error("Error in reading the moisture sensor")
        return moisture

    # this function might need to run for a period of time
    def output_RGB(self, colour, message):   #colour is a tuple of (255,255,255)
        grove_rgb_lcd.setRGB(*colour) 
        grove_rgb_lcd.setText(message)
        return

# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    grove = GrovePiInterface(timelimit=20)
    colour = (0,128,64)
    message = "this is working"
    grove.output_RGB(colour,message)
    #print(grove.read_light_sensor_analogueport(2))
