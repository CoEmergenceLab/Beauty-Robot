'''
This is a kind of dummy script that mimics one state-action pair of the Beauty robot's actions.
It mimics commands from the rl model's controller to select a pipette, collect attract/repellent solution
and drop it on the plate at a particular location (that the controller determines) before returning to
its home position.
'''


import os
import sys
import serial
import threading
from time import sleep
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI


# configure the Serial port
def serial_connect(port, baudrate=9600, timeout=1):
    ser = serial.Serial(
        # port='/dev/ttyS1',\
        port=port,\
        baudrate=baudrate,\
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
    swift.set_mode(0)  # normal mode

    # Get the initial position of the arm.
    position = swift.get_position(wait=True)
    print(position)

    # Set arm to home position
    HOME = (100, 0, 20)
    swift.set_buzzer(1000, 0.5)
    swift.set_wrist(90)
    print("moving arm to home position...")
    pos_status = swift.set_position(*HOME, speed=100, wait=True)  # Home
    print("pos_status: ", pos_status)
    sleep(1)

    # === INITIALIZE SERIAL COMMUNICATION WITH ARDUINO ===
    syringe_pump_serial = serial_connect("/dev/cu.usbmodem1411401", 19200, timeout=10)
    syringe_pump_serial.reset_output_buffer()

    # serial reader thread
    class SerialReaderThread(threading.Thread):
        def run(self):
            while True:
                # Read output from ser
                output = syringe_pump_serial.readline().decode('ascii')
                print(output)

    serial_reader = SerialReaderThread()
    serial_reader.start()

    syringe_pump_serial.write(b'S\n')  # put the steppers to sleep

    # === COORDINATES & AMOUNTS ===
    # pipette tip location coords
    tip_coords = ((120, -126.31, -56.55), (120, -126.31, -56.55), (120, -126.31, -56.55))
    tip_idx = 0

    # attractant/repellent locations and amounts (all amounts are in microliters)
    attractants = {
        "peptone" : ({"concentration" : "high", "amount" : 20, "location" : (165, -125.78, -52.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (125, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (125, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (125, -107.01, -41.37)}),
        "dextrose" : ({"concentration" : "high", "amount" : 20, "location" : (125, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (125, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (125, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (125, -113.47, -41.37)}),
        "lb" : ({"concentration" : "high", "amount" : 20, "location" : (130, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (130, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (130, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (130, -107.01, -41.37)}),
        "soc" : ({"concentration" : "high", "amount" : 20, "location" : (130, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 20, "location" : (130, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 5, "location" : (130, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 5, "location" : (130, -113.47, -41.37)})
    }
    repellents = {
        "co-trimoxazole" : ({"concentration" : "high", "amount" : 10, "location" : (135, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (135, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (135, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (135, -107.01, -41.37)}),
        "chloramphenicol" : ({"concentration" : "high", "amount" : 10, "location" : (135, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (135, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (135, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (135, -113.47, -41.37)}),
        "ampicillin" : ({"concentration" : "high", "amount" : 10, "location" : (140, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (140, -107.01, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (140, -103.78, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (140, -107.01, -41.37)}),
        "glacial acetic acid" : ({"concentration" : "high", "amount" : 10, "location" : (140, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 10, "location" : (140, -113.47, -41.37)},
                    {"concentration" : "high", "amount" : 1, "location" : (140, -110.24, -41.37)},
                    {"concentration" : "low", "amount" : 1, "location" : (140, -113.47, -41.37)})
    }

    # plate locations
    plate_coords = ((285, 0, -12), (290, 0, -12))

    # trash location
    trash_coords = (300, -150, 50)

    # === LOAD WORLD MODEL ===
    print("loading world model...")

    # === SET UP IMAGE CAPTURE ===
    # use Nikon DSLR/Mirrorless camera as a webcam
    print("camera ready...")

    # === CAPTURE IMAGES, DO MODEL PREDICTION & CONTROLLER ACTIONS ===
    # main program loop
    # capture a frame and show it to the rl model
    # (make sure camera is set to 1:1 ratio & check the dimensions of the frames to confirm)
    # then get an action from the model's controller
    # actions consist of location and attract/repellent (including amount and concentration)
    # can also be "null" or "None" action (i.e. do nothing)
    while True:
        # TODO - grab an image, show it to the world model and get an action
        # grab an image
        print("getting image...")
        # show image to world model & get action
        # this will inlcude the plate coords and the attractant/repellent to drop
        print("showing image to world model and getting next action...")

        sleep(1)

        print("moving arm into place...")
        swift.set_buzzer(1500, 0.25)
        swift.set_buzzer(1500, 0.25)
        # move arm to pipette tip location and pick up pipette tip
        swift.set_position(tip_coords[tip_idx][0],
                           tip_coords[tip_idx][1],
                           z=35.24,
                           speed=200,
                           timeout=30,
                           wait=True)  # current pipette tip location
        swift.set_position(z=tip_coords[tip_idx][2] + 19, speed=20, timeout=30, wait=True)  # acquire pipette
        swift.set_position(z=tip_coords[tip_idx][2] + 9, speed=2, wait=True)  # acquire pipette... slowly
        swift.set_position(z=tip_coords[tip_idx][2] + 4, speed=2, timeout=30, wait=True)  # acquire pipette
        swift.set_position(z=tip_coords[tip_idx][2], speed=1, timeout=30, wait=True)  # acquire pipette... got it
        sleep(1)
        swift.set_position(z=tip_coords[tip_idx][2] + 60, speed=2, timeout=30, wait=True)  # go back up
        sleep(0.1)
        swift.set_position(z=35.24, speed=200, timeout=30, wait=True)  # go back up
        sleep(1)

        # increment tip location
        tip_idx += 1

        # move arm to location of attractant/repellent selected by RL controller
        curr_solution_loc = attractants["peptone"][0]["location"]
        print("extracting attractant/repellent solution...")
        swift.set_position(x=curr_solution_loc[0],
                           y=curr_solution_loc[1],
                           z=30,
                           speed=200,
                           timeout=30,
                           wait=True)  # current attractant/repellent
        swift.set_position(z=curr_solution_loc[2] + 19, speed=20, timeout=30, wait=True)
        swift.set_position(z=curr_solution_loc[2] + 9, speed=3, timeout=30, wait=True)
        swift.set_position(z=curr_solution_loc[2] + 4, speed=3, timeout=30, wait=True)  # get closer
        swift.set_position(z=curr_solution_loc[2], speed=3, timeout=30, wait=True)  # ease in

        # TODO - need to control the syringe pump stepper
        # extract solution
        syringe_pump_serial.write(b's\n')  # take the steppers out of sleep mode
        sleep(1)
        syringe_pump_serial.write(b'+\n')  # extract
        sleep(3)

        swift.set_position(z=curr_solution_loc[2] + 60, speed=3, timeout=30, wait=True)  # go back up
        sleep(0.1)
        swift.set_position(z=30, speed=20, timeout=30, wait=True)  # go back up
        sleep(1)

        # move arm to location on plate (that you get from rl controller)
        print("dispensing attractant/repellent solution...")
        swift.set_position(x=plate_coords[0][0],
                           y=plate_coords[0][1],
                           z=25, speed=200,
                           timeout=30,
                           wait=True)  # current plate location
        swift.set_position(z=plate_coords[0][2] + 19, speed=20, timeout=30, wait=True)
        swift.set_position(z=plate_coords[0][2] + 9, speed=3, timeout=30, wait=True)
        swift.set_position(z=plate_coords[0][2] + 4, speed=3, timeout=30, wait=True)  # get closer
        swift.set_position(z=plate_coords[0][2], speed=3, timeout=30, wait=True)  # get ready to drop

        # TODO - need to control the syringe pump stepper
        # dispense solution
        syringe_pump_serial.write(b'-\n')  # dispense
        sleep(3)

        swift.set_position(z=plate_coords[0][2] + 40, speed=3, timeout=30, wait=True)  # go back up
        sleep(0.1)
        swift.set_position(z=50, speed=20, timeout=30, wait=True)  # go back up
        sleep(1)

        # move arm to trash location
        swift.set_position(x=trash_coords[0],
                           y=trash_coords[1],
                           z=75,
                           speed=200,
                           timeout=30,
                           wait=True)  # current plate location
        swift.set_position(z=trash_coords[2] + 19, speed=20, timeout=30, wait=True)
        swift.set_position(z=trash_coords[2], speed=5, timeout=30, wait=True)

        # TODO - connect pipette to servo
        # dispose of pipette
        swift.set_wrist(0, wait=True)
        sleep(1)
        swift.set_wrist(90, wait=True)
        sleep(1)
        swift.set_position(z=25, speed=20, timeout=30, wait=True)  # go back up
        sleep(1)

        # Go back to Home position
        print("moving arm back to home position...")
        swift.set_position(*HOME, speed=50, wait=True)  # Home

        print("dispensing soil remediatin solution...")
        # if image is considered more beautful to the AI than the previous image
        # then send solution via the soil stepper
        syringe_pump_serial.write(b'L\n')  # SOIL mode on
        sleep(0.1)
        syringe_pump_serial.write(b'+\n')  # dispense
        sleep(3)
        syringe_pump_serial.write(b'l\n')  # SOIL mode off
        sleep(0.1)

        syringe_pump_serial.write(b'S\n')  # put the steppers back to sleep

        # detach the uArm stepper motors
        print("putting the uArm to sleep...")
        swift.send_cmd_sync("M2019")

        # wait (30 minutes in the real system, 10 secs here for testing)
        print("waiting for next action...")
        sleep(10)

        # attach the uArm stepper motors
        print("waking up the uArm...")
        swift.send_cmd_sync("M17")


if __name__ == "__main__":
    main()
