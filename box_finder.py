import time
import random
import easygopigo3 as easy


def boxFinder():
    
    #point servo right and collect distance data
    servo.rotate_servo(0)
    right_obj_dist = dist_sensor.read()
    time.sleep(1)

    #point servo left and collect distance data
    servo.rotate_servo(180)
    left_obj_dist = dist_sensor.read()
    time.sleep(1)

    #recenter servo
    servo.reset_servo()
    sleep(1)

    #use data collected to determine if boxes exist
    if right_obj_dist <= BOX_DIST and left_obj_dist <= BOX_DIST:
        box_count += 2
        print("Boxes detected to the right and left!")
    elif left_obj_dist <= BOX_DIST:
        box_count += 1
        print("Box detected to the left.")
    elif right_obj_dist <= BOX_DIST:
        box_count += 1
        print("Box detected to the right.")
        
            
gpg = easy.EasyGoPiGo3() #instatiating EasyGoPiGo3 object
dist_sensor = gpg.init_distance_sensor() #instance of the Distance Sensor class
servo = gpg.init_servo() #instance of the Servo class
BOX_DIST = 100 #max distance of box detection in centimeters
forward_dist = 70 #distance car moves before stopping to scan for boxes

#put car in the default state
servo.reset_servo()
time.sleep(1)
gpg.stop()
box_count = 0

while True:

    #scan area for boxes
    boxFinder()
    
    #get distance of the object in front of the car
    obj_distance = dist_sensor.read()

    if obj_distance > forward_dist:
        gpg.drive_cm(forward_dist, True)
            
    #car has reached an obstacle, indicating this is the end of the route
    else:
        gpg.stop()
        print(box_count + " boxes were found!")
        break
    
    
