import grovepi
import time, math, sys, logging, threading
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease 
from di_sensors.temp_hum_press import TempHumPress
from grove_rgb_lcd import *

class GrovePiInterface():

    #Initialise log and timelimit (used to exit a function after time)
    def __init__(self, timelimit=20):
        self.logger = logging.getLogger()
        self.CurrentCommand = "loading"
        self.Configured = False #is the grove configured?

    # This function will return the current light reading from the desired ANALOG port A0, A1 etc
    def read_light_sensor_analogueport(self, port):
        light_sensor = port
        grovepi.pinMode(light_sensor,"INPUT")
        sensor_value = None
        try:
            sensor_value = grovepi.analogRead(light_sensor) # Get sensor value
        except IOError: #this doesnt appear to work
            log.error("Error in reading the light sensor")
        return sensor_value

    # This function will return the current light reading from the desired ANALOG port A0, A1 
    def read_ultra_digitalport(self, port):
        ultra = port
        grovepi.pinMode(ultra,"INPUT")
        sensor_value = None
        try:
            sensor_value = grovepi.ultrasonicRead(ultra) # Get sensor value
        except IOError: #this doesnt appear to work
            log.error("Error in reading the ultra sensor")
        return sensor_value

    #Turn on the led
    def turn_on_led_digitalport(self, port):
        led = port
        grovepi.pinMode(led,"OUTPUT")
        grovepi.digitalWrite(led,255)
        return

    #Turn off the led
    def turn_off_led_digitalport(self, port):
        led = port
        grovepi.pinMode(led,"OUTPUT")
        grovepi.digitalWrite(led,0)
        return

    #read temp and humidity
    def read_temp_humidity_sensor_digitalport(self, port):
        tempsensor = port
        grovepi.pinMode(tempsensor,"INPUT")
        temp_humidity_list = None
        try:
            temp_humidity_list = grovepi.dht(port,0) #0 - type blue sensor
        except IOError: #this doesnt appear to work
            log.error("Error in reading the temp and humidity sensor")
        return temp_humidity_list


    '''moisture=grovepi.analogRead(mositure_sensor)
	light=grovepi.analogRead(light_sensor)
	[temp,humidity] = grovepi.dht(temp_himidity_sensor,white)
		#Return -1 in case of bad temp/humidity sensor reading
	if math.isnan(temp) or math.isnan(humidity):		#temp/humidity sensor sometimes gives nan
			return [-1,-1,-1,-1]
		return [moisture,light,temp,humidity]

        pinMode(buzzer_pin,"OUTPUT")
        digitalWrite(buzzer_pin,1)
        digitalWrite(buzzer_pin,0)
        
        pinMode(button,"INPUT")		# Assign mode for Button as input
        button_status= digitalRead(button)
    '''

# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    grove = GrovePiInterface(timelimit=20)
    logger = logging.getLogger()
    logger.setLevel(logging.info)
    grove.set_log(logger)