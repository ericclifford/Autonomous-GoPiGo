import time
import random
from gopigo import *


def directionFinder():
    
    #point servo right and collect distance data
    servo(112)
    right_obj_dist = us_dist(15)
    time.sleep(0.5)

    #point servo left and collect distance data
    servo(28)
    left_obj_dist = us_dist(15)
    time.sleep(0.5)

    #recenter servo
    servo(70)
    sleep(0.5)
    # create some logic that uses the distances found above and possibly
    # where the car has already been to make a decision on which
    # direction to point the car next.

    if right_obj_dist > left_obj_dist and right_obj_dist > MIN_DISTANCE:
        right()
        
    elif left_obj_dist > right_obj_dist and left_obj_dist > MIN_DISTANCE:
        left()

    else:
        bwd()
        time.sleep(2)

        #prevents the car from backing up and going forward
        rot_choices = [right_rot, left_rot]
        rotation = rot_choices[random.randrange(0,2)]
        rotation()
        
def autonomy():

    while True:
        time.sleep(1)
        
        #gets distance of the object in front of the car
        obj_distance = us_dist(15)

        if obj_distance > MIN_DISTANCE:
            fwd()
        #object is too close, find a new path for the car
        else:
            stop()
            directionFinder()
            
MIN_DISTANCE = 70 #minium distance from object in centimeters

try:
    stop()
    enable_servo()
    servo(70)
    time.sleep(2)
    autonomy()
except:
    cleanup()
