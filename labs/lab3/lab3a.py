"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3A - Depth Camera Safety Stop
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

found_obstacle = False
was_ramp_counter = 0

# Add any global variables here

########################################################################################
# Functions
########################################################################################


def start():
    global found_obstacle
    global was_ramp_counter
    
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()

    found_obstacle = False
    was_ramp_counter = 0

    # Print start message
    print(
        ">> Lab 3A - Depth Camera Safety Stop\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Right bumper = override safety stop\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    A button = print current speed and angle\n"
        "    B button = print the distance at the center of the depth image"
    )


def update():
    global found_obstacle
    global was_ramp_counter
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # Use the triggers to control the car's speed
    # rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    # lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    # speed = rt - lt
    if found_obstacle:
        speed = 0
    else:
        speed = 1

    # Calculate the distance of the object directly in front of the car
    depth_image = rc.camera.get_depth_image()
    depth_image = (depth_image - 0.01) % 10000
    depth_image = depth_image[int(len(depth_image)/3) : len(depth_image) - 200, 225 : len(depth_image[0]) - 225]
    center_distance = rc_utils.get_depth_image_center_distance(depth_image)
    closest_pixel = rc_utils.get_closest_pixel(depth_image)

    top_pixel_dis = depth_image[int(len(depth_image)/2)][int(len(depth_image[0])/2)]
    lower_pixel_dis = depth_image[int(3/4 * len(depth_image))][int(len(depth_image[0])/2)]
    is_ramp = lower_pixel_dis < 9999 and top_pixel_dis < 9999 and (lower_pixel_dis + 1000) > top_pixel_dis > (lower_pixel_dis + 1)

    if is_ramp:
        was_ramp_counter += 1
    is_ramp = is_ramp or was_ramp_counter > 30

    # TODO (warmup): Prevent forward movement if the car is about to hit something.
    # Allow the user to override safety stop by holding the right bumper.
    if depth_image[closest_pixel[0]][closest_pixel[1]] < 100 and not rc.controller.was_pressed(rc.controller.Button.RB) and not is_ramp:
        found_obstacle = True
        speed = 0
        print(is_ramp)
        # print(str((lower_pixel_dis + 1000) > top_pixel_dis))
        # print(str(top_pixel_dis > (lower_pixel_dis + 1)))
        print(str(top_pixel_dis) + ' ' + str(lower_pixel_dis))
        print('found obstacle; stopping...')

    # Use the left joystick to control the angle of the front wheels
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]

    rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the depth image center distance when the B button is held down
    if rc.controller.is_down(rc.controller.Button.B):
        print("Center distance:", center_distance)

    # Display the current depth image
    rc.display.show_depth_image(depth_image)

    # TODO (stretch goal): Prevent forward movement if the car is about to drive off a
    # ledge.  ONLY TEST THIS IN THE SIMULATION, DO NOT TEST THIS WITH A REAL CAR.

    # TODO (stretch goal): Tune safety stop so that the car is still able to drive up
    # and down gentle ramps.
    # Hint: You may need to check distance at multiple points.


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
