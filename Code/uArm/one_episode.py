'''
This is a kind of dummy script that mimic one episode of the Beauty robot's actions.
It mimics commands from the rl model's controller to select a pipette, collect attract/repellent solution
and drop it on the plate at a particular location (that the controller determines) before returning to
its home position.
'''


import os
import sys
from time import sleep
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI


def main():
    print(__doc__)

    # === INITIALIZE ARM ===
    swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})

    sleep(2)
    print('device info: ')
    print(swift.get_device_info())
    swift.waiting_ready()
    swift.set_mode(0) # normal mode

    # Get the initial position of the arm.
    position = swift.get_position(wait=True)
    print(position)

    # Set arm to home position
    home = [60, 0, 30]
    swift.set_wrist(90)
    swift.set_position(home[0], home[1], home[2], speed=10000, wait=True) # Home

    # === LOAD WORLD MODEL ===

    # === SET UP IMAGE CAPTURE ===
    # use Nikon DSLR/Mirrorless camera as a webcam

    # === CAPTURE IMAGES,  DO MODEL PREDICTION & CONTROLLER ACTIONS ===
    # main program loop
    # capture a frame and show it to the rl model
    # (make sure camera is set to 1:1 ratio & check the dimensions of the frames to confirm)
    # then get an action from the model's controller
    # actions consist of location and attract/repellent (including amount and concentration)
    # can also be "null" or "None" action (i.e. do nothing)

    # move arm to pipette tip location and pick up pipette
    swift.set_position(75, -101.31, 40.24, speed=20000, timeout=30, wait=True)  # current pipette location
    swift.set_position(z=-15.5 speed=20000, timeout=30, wait=True)  # acquire pipette
    swift.set_position(z=-25, speed=200, timeout=30, wait=True)  # acquire pipette... slowly
    swift.set_position(z=-28, speed=200, timeout=30, wait=True)  # acquire pipette
    swift.set_position(z=-30, speed=200, timeout=30, wait=True)  # acquire pipette... got it
    sleep(0.1)
    swift.set_position(z=40.24, speed=20000, timeout=30, wait=True) # go back up

    # move arm to attractant/repellent location
    swift.set_position(x=165, y=-103.5, z=60, speed=20000, timeout=30, wait=True)  # current attractant/repellent loc
    swift.set_position(z=42, speed=20000, timeout=30, wait=True)  # get closer
    swift.set_position(z=38, speed=500, timeout=30, wait=True)  # ease in

    # extract solution
    # TODO - need to control the syringe pump stepper





if __name__ == "__main__":
    main()
