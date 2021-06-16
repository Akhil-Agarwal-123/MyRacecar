"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Phase 1 Challenge - Cone Slaloming
"""

########################################################################################
# Imports
########################################################################################

import sys
from enum import Enum
import copy

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

class State(Enum):
    RED_CONE_ON_SCREEN = 1,
    RED_CONE_OFF_SCREEN_MOVE_AWAY = 2,
    SEARCHING_AFTER_RED = 3,
    BLUE_CONE_ON_SCREEN = 4,
    BLUE_CONE_OFF_SCREEN_MOVE_AWAY = 5,
    SEARCHING_AFTER_BLUE = 6,
    SEARCHING = 7

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

MIN_CONTOUR_AREA = 1000

BLUE = ((90, 100, 50), (120, 255, 255))
RED = ((0, 50, 20), (50, 255, 255))
RED2 = ((160, 50, 20), (179, 255, 255))

COLORS = (BLUE, RED, RED2)

color_image = None
contour_center = None
contour_area = None

cur_state = None
timer = None

# Add any global variables here

########################################################################################
# Functions
########################################################################################

def update_contour():
    """
    Finds contours in the current color image and uses them to update contour_center
    and contour_area
    """
    global contour_center
    global contour_area
    global color_image

    image = rc.camera.get_color_image()
    image = image[len(image)//3:]

    if image is None:
        contour_center = None
        contour_area = 0
        contour = None
        color_image = None
    else:
        color_image = copy.deepcopy(image)
        final_contours = []

        for COLOR_RANGE in COLORS:
            # Find all of the blue contours
            contours = rc_utils.find_contours(image, COLOR_RANGE[0], COLOR_RANGE[1])

            # Select the largest contour
            largest_contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)
            if largest_contour is not None:
                final_contours.append(rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA))
        
        contour = rc_utils.get_largest_contour(final_contours, MIN_CONTOUR_AREA)

        if contour is not None:
            # Calculate contour information
            contour_center = rc_utils.get_contour_center(contour)
            contour_area = rc_utils.get_contour_area(contour)

            # Draw contour onto the image
            rc_utils.draw_contour(image, contour)
            rc_utils.draw_circle(image, contour_center)

        else:
            contour_center = None
            contour_area = 0

        # Display the image to the screen
        rc.display.show_color_image(image)
    

def is_blue(bgr_value):
    return 100 < bgr_value[0]


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Have the car begin at a stop
    rc.drive.stop()

    global timer, cur_state, color_image, contour_center, contour_area
    timer = 0.0
    cur_state = State.SEARCHING
    color_image = None
    contour_center = None
    contour_area = None

    # Print start message
    print(">> Phase 1 Challenge: Cone Slaloming")


def update_timer():
    global timer
    timer += rc.get_delta_time()


def update():
    global timer, cur_state, color_image, contour_center, contour_area
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Slalom between red and blue cones.  The car should pass to the right of
    # each red cone and the left of each blue cone.
    update_contour()
    update_timer()

    if color_image is not None:
        speed = 1
        angle = None
        if contour_center is not None:
            kpa = 1.0

            depth_image = rc.camera.get_depth_image()
            depth_image = depth_image[len(depth_image)//3:]
            distance = depth_image[contour_center[0]][contour_center[1]]

            color = color_image[contour_center[0]][contour_center[1]]

            blue = False
            red = False

            print(color)

            if is_blue(color):
                blue = True
                print('looks blue')
                if (cur_state == State.SEARCHING_AFTER_RED) or (cur_state == State.SEARCHING and distance < 120):
                    cur_state = State.BLUE_CONE_ON_SCREEN
                    timer = 0.0
            else:
                red = True
                print('looks red')
                if (cur_state == State.SEARCHING_AFTER_BLUE) or (cur_state == State.SEARCHING and distance < 120):
                    cur_state = State.RED_CONE_ON_SCREEN
                    timer = 0.0

            if cur_state == State.BLUE_CONE_ON_SCREEN:
                angle = -1
            if cur_state == State.RED_CONE_ON_SCREEN:
                angle = 1
            
            if distance > 125 and ((cur_state == State.BLUE_CONE_ON_SCREEN and blue) or (cur_state == State.RED_CONE_ON_SCREEN and red)):
                angle = max(-1, min(kpa * (contour_center[1] - (rc.camera.get_width() / 2)), 1))

        if contour_center is None:
            if cur_state == State.RED_CONE_ON_SCREEN:
                cur_state = State.RED_CONE_OFF_SCREEN_MOVE_AWAY
                timer = 0.0
            
            if cur_state == State.BLUE_CONE_ON_SCREEN:
                cur_state = State.BLUE_CONE_OFF_SCREEN_MOVE_AWAY
                timer = 0.0
        
        if cur_state == State.RED_CONE_OFF_SCREEN_MOVE_AWAY:
            if timer > 0.35:
                cur_state = State.SEARCHING_AFTER_RED
                timer = 0.0
            else:
                angle = 1
        
        if cur_state == State.BLUE_CONE_OFF_SCREEN_MOVE_AWAY:
            if timer > 0.35:
                cur_state = State.SEARCHING_AFTER_BLUE
                timer = 0.0
            else:
                angle = -1
        
        if cur_state == State.SEARCHING:
            angle = 0
        
        if cur_state == State.SEARCHING_AFTER_RED:
            angle = -1
        
        if cur_state == State.SEARCHING_AFTER_BLUE:
            angle = 1
        
        print(cur_state)
        rc.drive.set_speed_angle(speed, angle)
    else:
        rc.drive.stop()


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
