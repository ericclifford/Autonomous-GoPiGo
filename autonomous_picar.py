import time
import random
import easygopigo3 as easy


def directionFinder():
    
    #point servo right and collect distance data
    servo.rotate_servo(0)
    right_obj_dist = dist_sensor.read()
    time.sleep(0.5)

    #point servo left and collect distance data
    servo.rotate_servo(180)
    left_obj_dist = dist_sensor.read()
    time.sleep(0.5)

    #recenter servo
    servo.reset_servo()
    sleep(0.5)
    # create some logic that uses the distances found above and possibly
    # where the car has already been to make a decision on which
    # direction to point the car next.

    if right_obj_dist > left_obj_dist and right_obj_dist > MIN_DISTANCE:
        gpg.right()
        
    elif left_obj_dist > right_obj_dist and left_obj_dist > MIN_DISTANCE:
        gpg.left()

    else:
        gpg.backward()
        time.sleep(2)

        #prevents the car from backing up and going forward
        rot_choices = [90, -90]
        rotation = rot_choices[random.randrange(0, 2)]
        gpg.turn_degrees(rotation)
        
def autonomy():

    while True:
        time.sleep(1)
        
        #gets distance of the object in front of the car
        obj_distance = dist_sensor.read()

        if obj_distance > MIN_DISTANCE:
            gpg.forward()
        #object is too close, find a new path for the car
        else:
            gpg.stop()
            directionFinder()
            
MIN_DISTANCE = 70 #minium distance from object in centimeters
gpg = easy.EasyGoPiGo3() #instatiating a EasyGoPiGo3 object
dist_sensor = gpg.init_distance_sensor() #instance of the Distance Sensor class
servo = gpg.init_servo() #instance of the Servo class
try:
    gpg.stop()
    servo.reset_servo()
    time.sleep(2)
    autonomy()
except:
    cleanup()
