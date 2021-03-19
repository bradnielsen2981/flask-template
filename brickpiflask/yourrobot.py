import time, math, os, sys, logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import globalvars
from brickpiflask.interfaces.brickpiinterface import *
from brickpiflask.interfaces.soundinterface import * 
import helpers

DATABASE = globalvars.DATABASE #create alias for DATABASE
SOUND = globalvars.SOUND

#Use this class to inherit the code from BrickPiInterface, add to and redefine functions
class Robot(BrickPiInterface):

    def __init__(self, timelimit=20, logger=logging.getLogger()):
        super().__init__(timelimit, logger)
        #self.CurrentCommand = "stop"
        self.CurrentRoutine = "stop"
        self.data = None
        return


    #Create a function to move forward until object detected
    #Need to return some data which can be used
    def move_power_time_until_detect_object(self, power, t, distance=20, deviation=0):
        bp = self.BP #alias
        
        self.interrupt_previous_command()
        self.CurrentCommand = "move_power_time_until_detect_object"

        #dictionary
        data = {'action':self.CurrentCommand,'elapsed':0,'distancedetected':0,'colourdetected':None} #return data

        #check to see if vital sensors working
        if self.config['ultra'] >= SensorStatus.DISABLED:
            return data

        #create timelimit
        starttime = time.time()
        timelimit = starttime + t

        #start motors
        bp.set_motor_power(self.rightmotor, power)
        bp.set_motor_power(self.leftmotor, power + deviation)

        while ((time.time() < timelimit) and (self.CurrentCommand == "move_power_time_until_detect_object")):

            #detect an object using ultrasonic
            distancetoobject = self.get_ultra_sensor()
            print(distancetoobject)
            if ((distancetoobject < distance) and (distancetoobject != 0)): #check that its not an invalid reading
                data['distancedetected'] = distancetoobject
                break
            
            #detect a colour using colour sensor
            colour = self.get_colour_sensor()
            data['colourdetected'] = colour

        self.stop_all()
        data['elapsed'] = time.time() - starttime
        return data
    

    #Create a function to move forward until object detected
    #Need to return some data which can be used
    def rotate_power_degrees_IMU_until_detect_object(self, power, degrees, distance, marginoferror=3):
        bp = self.BP #alias

        #interrupt the current command
        self.interrupt_previous_command()
        self.CurrentCommand = "rotate_power_degrees_IMU_until_detect_object"
        data = {'action':self.CurrentCommand,'rotated':0,'distancedetected':0,'elapsed':0} #return data

        #check to see if sensors working
        if (self.config['ultra'] >= SensorStatus.DISABLED) or (self.config['imu'] >= SensorStatus.DISABLED):
            return data
        
        symbol = '<'; limit = 0
        if degrees == 0:
            return
        elif degrees < 0:
            symbol = '>='; limit = degrees+marginoferror
        else:
            symbol = '<='; limit = degrees-marginoferror; power = -power
        totaldegreesrotated = 0; lastrun = 0
        
        starttime = time.time(); timelimit = starttime + self.timelimit

        #set motors with one motor in reverse
        bp.set_motor_power(self.rightmotor, power)
        bp.set_motor_power(self.leftmotor, -power)

        while eval("totaldegreesrotated" + str(symbol) + "limit") and (self.CurrentCommand == "rotate_power_degrees_IMU_until_detect_object") and (time.time() < timelimit):

            lastrun = time.time()
            gyrospeed = self.get_gyro_sensor_IMU()[2] #rotate around z-axis

            #detect object
            distancetoobject = self.get_ultra_sensor()
            print(distancetoobject)
            if ((distancetoobject < distance) and (distancetoobject != 0)):
                data['distancedetected'] = distancetoobject
                break

            totaldegreesrotated += (time.time() - lastrun)*gyrospeed
        self.stop_all()
        data['rotated'] = totaldegreesrotated
        data['elapsed'] = time.time() - starttime
        data['heading'] = self.get_compass_IMU()
        return data

    #repeatedly search in a circle, move forward when object is detected...
    def automated_search_and_retrieval(self):
        if SOUND:
            SOUND.say("AUTOMATED SEARCH ENABLED.")
        self.CurrentRoutine = "automated_search_and_retrieval" #create a routine

        self.data = self.rotate_power_degrees_IMU_until_detect_object(20, 360, 40)
        self.data['heading'] = self.get_compass_IMU() #uses compass values IMUS
        self.data['sequence'] = 1
        #Save to Database

        self.data = self.move_power_time_until_detect_object(30, 4, 15)
        self.data['heading'] = self.get_compass_IMU() #uses compass values IMUS
        self.data['sequence'] = 2
        #Save to Database

        return

        
#Load the brickpi
def load_robot(timelimit, logger):
    robot = Robot(timelimit, logger)
    global SOUND
    SOUND = SoundInterface()
    SOUND.say("I am ready.")
    return robot

#--------------------------------------------------------------------
# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    SOUND = SoundInterface()
    SOUND.say("I will destroy you!")
    robot = Robot(20, logging.getLogger())  #20 second timelimit before
    bp = robot.BP #alias to shorten code
    robot.BP.reset_all()
    motorports = {'rightmotor':bp.PORT_B, 'leftmotor':bp.PORT_C, 'mediummotor':bp.PORT_D }
    sensorports = {'thermal':None,'colour':bp.PORT_1,'ultra':bp.PORT_4,'imu':1 }
    robot.configure_sensors(motorports, sensorports) #This takes 4 seconds
    robot.log("HERE I AM")
    input("Press any key to test: ")
    #robot.rotate_power_degrees_IMU(30, 180)
    #robot.move_power_time(30, 2)
    data = robot.automated_search_and_retrieval()
    print(robot.get_all_sensors())
    robot.safe_exit()