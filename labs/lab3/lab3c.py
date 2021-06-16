"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3C - Depth Camera Wall Parking
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np
import math

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Add any global variables here
prev_dis = 0.0
prev_sign = 0
oscillation_counter = 0

########################################################################################
# Functions
########################################################################################


def start():
    global prev_dis
    global prev_sign
    global oscillation_counter
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()
    prev_dis = 0.0
    prev_sign = 0
    oscillation_counter = 0

    # Print start message
    print(">> Lab 3C - Depth Camera Wall Parking")


def update():
    global prev_dis
    global prev_sign
    global oscillation_counter
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Park the car 20 cm away from the closest wall with the car directly facing
    # the wall

    depth_image = rc.camera.get_depth_image()
    depth_image = (depth_image - 0.01) % 10000
    depth_image = depth_image[int(len(depth_image)/3) : len(depth_image) - 225]
    closest_point = rc_utils.get_closest_pixel(depth_image)

    kpa = 0.0005
    angle = max(-1, min(kpa * (closest_point[1] - (rc.camera.get_width() / 2)), 1))

    kps = 2
    cur_dis = depth_image[closest_point[0]][closest_point[1]] - 20
    speed = kps * cur_dis
    delta_time = rc.get_delta_time()
    accel = min(1, max(-1, kps * (speed - ((prev_dis - cur_dis)/delta_time))))
    prev_dis = cur_dis

    if accel < 0:
        angle *= -1
    
    print(accel)
    print(angle)

    if abs(angle) > 0.05 and oscillation_counter < 10:
        if accel > 0:
            angle *= -1
        accel = -1
        angle = math.copysign(0.5, angle)
    
    if math.copysign(1, angle) != prev_sign and prev_sign != 0:
        oscillation_counter += 1
    
    prev_sign = math.copysign(1, angle)
    
    print(accel)
    print(angle)
    print('-------------')

    rc.drive.set_speed_angle(accel, angle)
    rc.display.show_depth_image(depth_image)


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
