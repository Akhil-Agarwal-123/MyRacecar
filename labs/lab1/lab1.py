"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 1 - Driving in Shapes
"""

########################################################################################
# Imports
########################################################################################

import sys

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Put any global variables here

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Begin at a full stop
    rc.drive.stop()

    # Print start message
    # TODO (main challenge): add a line explaining what the Y button does
    print(
        ">> Lab 1 - Driving in Shapes\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    A button = drive in a circle\n"
        "    B button = drive in a square\n"
        "    X button = drive in a figure eight\n"
    )

driving_in_circle = False

driving_in_square = False
square_stage = 0

driving_in_8 = False
figure_8_stage = 0

driving_in_random = False

timer = 0


def update():
    global driving_in_circle
    global driving_in_square
    global driving_in_8
    global driving_in_random
    global square_stage
    global figure_8_stage
    global timer

    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    speed = 0
    angle = 0

    # TODO (warmup): Implement acceleration and steering
    # rc.drive.set_speed_angle(0, 0)
    if rc.controller.get_trigger(rc.controller.Trigger.RIGHT) == 1:
        speed = 1
    if rc.controller.get_trigger(rc.controller.Trigger.LEFT) == 1:
        speed = -1
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]

    if rc.controller.was_pressed(rc.controller.Button.A):
        print("Driving in a circle...")
        # TODO (main challenge): Drive in a circle
        driving_in_circle = True
        timer = 0
    
    if driving_in_circle:
        speed = 1
        angle = 1
        
        if timer > 5.5:
            driving_in_circle = False
            speed = -1

    # TODO (main challenge): Drive in a square when the B button is pressed
    if rc.controller.was_pressed(rc.controller.Button.B):
        print("Driving in a square...")
        driving_in_square = True
        timer = 0
        square_stage = 0
    
    if driving_in_square:
        if square_stage % 2 == 0:
            speed = 1
            angle = 0
        
        if square_stage % 2 == 1:
            angle = 0.85
            speed = 0.7
        
        case1Square = ((square_stage == 0) and (timer > 1.5))
        case2Square = ((square_stage != 0) and (square_stage % 2 == 0) and (timer > 0.5))
        case3Square = ((square_stage == 7) and (timer > 1))
        case4Square = ((square_stage != 7) and (square_stage % 2 == 1) and (timer > 1.75))
        if case1Square or case2Square or case3Square or case4Square:
            square_stage += 1
            timer = 0
        
        if square_stage == 8:
            driving_in_square = False
    
    # TODO (main challenge): Drive in a figure eight when the X button is pressed
    if rc.controller.was_pressed(rc.controller.Button.X):
        print("Driving in a figure 8...")
        driving_in_8 = True
        timer = 0
        figure_8_stage = 0
    
    if driving_in_8:
        if figure_8_stage == 0:
            speed = 1
            angle = 0.3
        
        if figure_8_stage > 0:
            speed = 1
            if figure_8_stage % 4 == 1:
                angle = -1
            elif figure_8_stage % 4 == 2:
                angle = 0
            elif figure_8_stage % 4 == 3:
                angle = 1
            else:
                angle = 0
        
        if figure_8_stage == 0 and timer > 2.75:
            figure_8_stage += 1
            timer = 0

        if figure_8_stage > 0 and (figure_8_stage % 4 == 0 or figure_8_stage % 4 == 2) and timer > 2:
            figure_8_stage += 1
            timer = 0
        
        if figure_8_stage > 0 and figure_8_stage % 4 != 2 and figure_8_stage % 4 != 0 and timer > 3.5:
            figure_8_stage += 1
            timer = 0
        
        if figure_8_stage == 7:
            driving_in_8 = False
            speed = -1

    # TODO (main challenge): Drive in a shape of your choice when the Y button
    # is pressed
    if rc.controller.was_pressed(rc.controller.Button.Y):
        driving_in_random = True
        timer = 0
    
    if driving_in_random:
        speed = 1
        angle = 0
        if timer > 3:
            driving_in_random = False

    timer += rc.get_delta_time()
    rc.drive.set_speed_angle(speed, angle)


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
