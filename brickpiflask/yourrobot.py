import time, math, os, sys, logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import globalvars
from brickpiflask.interfaces.brickpiinterface import *
import helpers

DATABASE = globalvars.DATABASE #create alias for DATABASE

#Use this class to inherit the code from BrickPiInterface, add to and redefine functions
class Robot(BrickPiInterface):

    def __init__(self, timelimit=20, logger=logging.getLogger()):
        super().__init__(timelimit, logger)
        self.CurrentRoutine = "none"
        return


#Create a function based on move_power_time to move until detect object or colour



#Create a function to rotate until detect object and then check its temperature



#Create a function reverse actions taken or calculate fastest route to base using trig



#Load the brickpi
def load_robot(timelimit, logger):
    robot = Robot(timelimit, logger)
    return robot

#--------------------------------------------------------------------
# Only execute if this is the main file, good for testing code
if __name__ == '__main__':
    robot = Robot(timelimit=20)  #20 second timelimit before
    bp = robot.BP #alias to shorten code
    motorports = {'rightmotor':bp.PORT_B, 'leftmotor':bp.PORT_C, 'mediummotor':bp.PORT_D }
    sensorports = { 'thermal':bp.PORT_2,'colour':bp.PORT_1,'ultra':bp.PORT_4,'imu':1 }
    robot.configure_sensors(motorports, sensorports) #This takes 4 seconds
    robot.log("HERE I AM")
    input("Press any key to test: ")
    robot.move_power_time(50, 3, deviation=5) #deviation 5 seems work well, if reversing deviation needs to also reverse
    print("HELLO")
    print(robot.get_all_sensors())
    robot.safe_exit()