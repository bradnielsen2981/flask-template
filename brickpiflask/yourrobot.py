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
        self.interrupt_previous_command()
        self.CurrentCommand = "move_power_time_until_detect_object"

        self.stop_all()
        return data
    

    #Create a function to move forward until object detected
    #Need to return some data which can be used
    def rotate_power_degrees_IMU_until_detect_object(self, power, degrees, distance, marginoferror=3):
        #interrupt the current command
        self.interrupt_previous_command()
        self.CurrentCommand = "rotate_power_degrees_IMU_until_detect_object"
        
        self.stop_all()
        return data

    #repeatedly search in a circle, move forward when object is detected...
    def automated_search_and_retrieval(self):
        self.interrupt_previous_command()
        self.CurrentRoutine = "automated_search_and_retrieval" #create a routine

        self.stop_all()
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
