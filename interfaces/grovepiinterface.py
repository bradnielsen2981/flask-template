import grovepi
import time, math, sys, logging, threading
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease 
from di_sensors.temp_hum_press import TempHumPress
import grove_rgb_lcd

class GrovePiInterface():

    #Initialise log and timelimit (used to exit a function after time)
    def __init__(self, timelimit=20):
        self.logger = logging.getLogger()
        self.timelimit = timelimit
        self.CurrentCommand = "loading"
        self.Configured = True #is the grove configured? All ports should be configured
        self.lightswitch = False
        return

        #changes the logger
    def set_log(self, logger):
        self.logger=logger
        return

    # This function will return the current light reading from the desired ANALOG port A0
    def read_light_sensor_analogueport(self, port):
        if not self.Configured:
            return -1
        grovepi.pinMode(port,"INPUT")
        sensor_value = None
        try:
            sensor_value = grovepi.analogRead(port) # Get sensor value
        except IOError: #this doesnt appear to work
            self.log("Error in reading the light sensor")
        return sensor_value

    # This function will return the current ultrasonic from the digital port
    def read_ultra_digitalport(self, port):
        if not self.Configured:
            return -1
        grovepi.pinMode(port,"INPUT")
        sensor_value = None
        try:
            sensor_value = grovepi.ultrasonicRead(port) # Get sensor value
        except IOError: #this doesnt appear to work
            self.log("Error in reading the ultra sensor")
        return sensor_value

    # Turn on the led using digital port 
    def switch_led_digitalport_value(self, port, value):
        if not self.Configured:
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
    def read_temp_humidity_sensor_digitalport(self, port):
        if not self.Configured:
            return -1
        grovepi.pinMode(port,"INPUT")
        temp_humidity_list = None
        try:
            temp_humidity_list = grovepi.dht(port,0) #0 - type blue sensor
        except IOError: #this doesnt appear to work
            self.log("Error in reading the temp and humidity sensor")
        return temp_humidity_list

    # Get the current moisture
    def read_moisture_sensor_analogueport(self, port):
        if not self.Configured:
            return -1
        grovepi.pinMode(port,"INPUT")
        moisture = None
        try:
            moisture = grovepi.analogRead(port)
        except IOError: #this doesnt appear to work
            self.log("Error in reading the moisture sensor")
        return moisture

    # this function might need to run for a period of time
    def output_RGB(self, colour, message): #colour tuple (255,255,255)
        if not self.Configured:
            return -1
        grove_rgb_lcd.setRGB(*colour) 
        grove_rgb_lcd.setText(message)
        return

        #log out whatever !!!!!THIS IS NOT WORKING UNLESS FLASK LOG USED??
    def log(self, message):
        self.logger.error(message)
        return

# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    grove = GrovePiInterface(timelimit=20)
    colour = (0,128,64)
    message = "this is working"
    grove.output_RGB(colour,message)
    print(grove.read_light_sensor_analogueport(2))
