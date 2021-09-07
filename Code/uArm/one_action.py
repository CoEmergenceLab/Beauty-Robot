'''
This is a kind of dummy script that mimics one state-action pair of the Beauty robot's actions.
It mimics commands from the rl model's controller to select a pipette, collect attract/repellent solution
and drop it on the plate at a particular location (that the controller determines) before returning to
its home position.
'''


import os
import sys
import serial
from time import sleep
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI



# configure the Serial port
def serial_connect(port, baudrate=9600, timeout=1):
	ser = serial.Serial(
	    # port='/dev/ttyS1',\
        port=port,\
	    baudrate=baud,\
	    parity=serial.PARITY_NONE,\
	    stopbits=serial.STOPBITS_ONE,\
	    bytesize=serial.EIGHTBITS,\
	    timeout=timeout)
	print("Connected to: " + ser.portstr)
	return ser


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
    HOME = (66, 0, 30)
    swift.set_wrist(90)
    swift.set_position(*HOME, speed=10000, wait=True) # Home

    # === INITIALIZE SERIAL COMMUNICATION WITH SYRINGE PUMP ===
    syringe_pump_serial = serial_connect("/dev/cu.URT1", 9600)

    # === COORDINATES & AMOUNTS ===
    # pipette tip location coords
    tip_coords = ((80, -101.31, -39.11), (80, -101.31, -39.11))
    tip_idx = 0

    # attractant/repellent locations and amounts (all amounts are in microliters)
    attractants = {
        "peptone" : ({"concentration" : "high", "amount" : 20, "location" : (95, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (95, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (95, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (95, -107.01, -41.37)}),
        "dextrose" : ({"concentration" : "high", "amount" : 20, "location" : (95, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (95, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (95, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (95, -113.47, -41.37)}),
        "lb" : ({"concentration" : "high", "amount" : 20, "location" : (100, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (100, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (100, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (100, -107.01, -41.37)}),
        "soc" : ({"concentration" : "high", "amount" : 20, "location" : (100, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (100, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (100, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (100, -113.47, -41.37)})
    }
    repellents = {
        "co-trimoxazole" : ({"concentration" : "high", "amount" : 10, "location" : (105, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (105, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (105, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (105, -107.01, -41.37)}),
        "chloramphenicol" : ({"concentration" : "high", "amount" : 10, "location" : (105, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (105, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (105, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (105, -113.47, -41.37)}),
        "ampicillin" : ({"concentration" : "high", "amount" : 10, "location" : (110, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (110, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (110, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (110, -107.01, -41.37)}),
        "glacial acetic acid" : ({"concentration" : "high", "amount" : 10, "location" : (110, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (110, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (110, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (110, -113.47, -41.37)})
    }

    # plate locations
    plate_coords = ((90, 0, -42), (90, 0, -42))

    # trash location
    trash_coords = (120, -115, -20)

    # === LOAD WORLD MODEL ===

    # === SET UP IMAGE CAPTURE ===
    # use Nikon DSLR/Mirrorless camera as a webcam
    # TODO - take a photo before we start loop
    print("getting first image...")
    photo_taken = True
    print("first image acquired, waiting for 30 minutes...")
    sleep(10) # wait (30 minutes in the real system, 10 secs here for testing)

    # === CAPTURE IMAGES,  DO MODEL PREDICTION & CONTROLLER ACTIONS ===
    # main program loop
    # capture a frame and show it to the rl model
    # (make sure camera is set to 1:1 ratio & check the dimensions of the frames to confirm)
    # then get an action from the model's controller
    # actions consist of location and attract/repellent (including amount and concentration)
    # can also be "null" or "None" action (i.e. do nothing)
    while True:
        if photo_taken:
            # TODO - get image and show it to the ml model and get the prediction
            # this will inlcude the plate coords and the attractant/repellent to drop
            # then set photo_taken to False
            photo_taken = False
        else:
            # TODO - take a photo before and wait for 30 minutes
            print("getting image...")
            photo_taken = True
            print("image acquired, waiting for 30 minutes...")
            sleep(10) # wait (30 minutes in the real system, 10 secs here for testing)
            # TODO - show image to the ml model and get the prediction
            # this will inlcude the plate coords and the attractant/repellent to drop
            # then set photo_taken to False
            photo_taken = False

        # move arm to pipette tip location and pick up pipette
        swift.set_position(tip_coords[tip_idx][0],
                        tip_coords[tip_idx][1],
                        z=35.24,
                        speed=20000,
                        timeout=30,
                        wait=True)  # current pipette location
        swift.set_position(z=tip_coords[tip_idx][2] + 19 speed=20000, timeout=30, wait=True)  # acquire pipette
        swift.set_position(z=tip_coords[tip_idx][2] + 9, wait=True)  # acquire pipette... slowly
        swift.set_position(z=tip_coords[tip_idx][2] + 4, speed=200, timeout=30, wait=True)  # acquire pipette
        swift.set_position(z=tip_coords[tip_idx][2], speed=200, timeout=30, wait=True)  # acquire pipette... got it
        sleep(0.1)
        swift.set_position(z=35.24, speed=20000, timeout=30, wait=True) # go back up
        # increment tip location
        tip_idx += 1

        # move arm to location of attractant/repellent selected by RL controller
        curr_solution_loc = attractants["peptone"][0]["location"]
        swift.set_position(x=curr_solution_loc[0],
                        y=curr_solution_loc[1],
                        z=30,
                        speed=20000,
                        timeout=30,
                        wait=True)  # current attractant/repellent
        swift.set_position(z=curr_solution_loc[2] + 19, speed=20000, timeout=30, wait=True)
        swift.set_position(z=curr_solution_loc[2] + 9, speed=300, timeout=30, wait=True)
        swift.set_position(z=curr_solution_loc[2] + 4, speed=300, timeout=30, wait=True)  # get closer
        swift.set_position(z=curr_solution_loc[2], speed=300, timeout=30, wait=True)  # ease in

        # TODO - need to control the syringe pump stepper
        # extract solution

        sleep(0.1)
        swift.set_position(z=30, speed=20000, timeout=30, wait=True) # go back up


        # move arm to location on plate (that you get from rl controller)
        swift.set_position(x=plate_coords[0][0],
                        y=plate_coords[0][1],
                        z=25,
                        speed=20000,
                        timeout=30,
                        wait=True)  # current plate location
        swift.set_position(z=plate_coords[0][2] + 19, speed=20000, timeout=30, wait=True)
        swift.set_position(z=plate_coords[0][2] + 9, speed=300, timeout=30, wait=True)
        swift.set_position(z=plate_coords[0][2] + 4, speed=300, timeout=30, wait=True) # get closer
        swift.set_position(z=plate_coords[0][2], speed=300, timeout=30, wait=True) # get ready to drop

        # TODO - need to control the syringe pump stepper
        # dispense solution

        sleep(0.1)
        swift.set_position(z=25, speed=20000, timeout=30, wait=True) # go back up

        # move arm to trash location
        swift.set_position(x=trash_coords[0],
                        y=trash_coords[1],
                        z=30,
                        speed=20000,
                        timeout=30,
                        wait=True)  # current plate location
        swift.set_position(z=trash_coords[2] + 19, speed=20000, timeout=30, wait=True)
        swift.set_position(z=trash_coords[2], speed=500, timeout=30, wait=True)

        # TODO - connect pipette to servo
        # dispose of pipette
        swift.set_wrist(0, wait=True)
        sleep(1)
        swift.set_wrist(90, wait=True)
        sleep(1)
        swift.set_position(z=25, speed=20000, timeout=30, wait=True) # go back up

        # Go back to Home position
        swift.set_position(*HOME, speed=10000, wait=True) # Home



if __name__ == "__main__":
    main()
