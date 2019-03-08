import math
import time
import easygopigo3 as easy

#positions servo and collects/returns distance data
def distance_finder(servo_position):
    servo.rotate_servo(servo_position)
    time.sleep(0.25)
    obj_distance = dist_sensor.read()
    #frontward object distance
    if servo_position == 90:
        return object_dist
    #rightward object distance
    else:
        return object_distance * math.sin(servo_position)


def route_car(move_dist):
    gpg.move_cm(move_dist, False)
    time.sleep(0.5)
    #loop executes until car comes to a stop
    while gpg.get_speed > 0:
        current_time_moving += time.time()
        #approaching a box. continusly scan forward until box is reached
        if approaching_box:
            object_distance = scan(90)
            #path is ending. stop car
            if object_distance <= MIN_DETECTION_RANGE:
                print("Object detected in front of car.")
                return 0
        #not approaching box. continusly scan 30, 60, and 90 degrees until a box is found or path ends
        elif not approaching_box:
            object_distance = scan( servo_position = servo_position % 90 + 30 )
            #path is ending. stop car
            if servo_position == 90 and object_distance <= MIN_DETECTION_RANGE:
                print("Object detected in front of car.")
                return 0
            #a box was located in detectable range. position car beside it.
            elif servo_position != 90 and object_distance <= MAX_BOX_DETECTION_RANGE:
                print("Box has been detected.")
                box_count += 1
                approaching_box = True
                gpg.move_cm(object_distance, False)
            #box not found and end of path has not been reached. continue forward
            else:
                gpg.foward()
    #box has been reached. stop car.
    return MAX_DETECTION_RANGE
	
gpg = easy.EasyGoPiGo3() #instatiating EasyGoPiGo3 object
dist_sensor = gpg.init_distance_sensor() #instance of the Distance Sensor class
servo = gpg.init_servo() #instance of the Servo class
servo.rest()
servo_position = 60 #degrees
MAX_DETECTION_RANGE = 150 #cm
MIN_DETECTION_RANGE = 30 #cm
box_count = 0
first_pass_time = -1 #inialize to a number greater than 0
current_time_moving = 0

#program executes until robot car returns to its starting position
while current_time_moving != first_pass_time:
    
    approaching_box = False #is the car currently approaching a detected box
    fwd_distance = distance_finder(90)

    #not at the end of path. continue forward
    if fwd_distance > MIN_DETECTION_RANGE:
        print("Car has started moving forward.")
        fwd_distance = route_car(fwd_distance)
    elif fwd_distance <= MIN_DETECTION_RANGE and current_time_moving == 0:
        print("Car cannot begin route because object is blocking the way.")
    #car has reached the end of the path
    else:
        print("Car is turning around.")
        gpg.turn_degrees(180)
        first_pass_time = current_pass_time
        current_time_moving = 0
        
    print("Car is stopped.")

print("Car has returned to starting position." + box_count + " boxes found.")
