import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

import serial

# @brief: Send a read/write command to the Arduino
# @par ser: The serial port instance
# @par command: The name of the read/write command
# @ret None
def send_command(ser, command):
	ser.write(command.encode())

# @brief: Check and wait for the Acknowledgeent from the Arduino
# @par ser: The serial port instance
# @par ack_string: The name of the acknowledgement message
# @ret: None	
def check_ack(ser, ack_string):	
	while(1):
		recd_ack = ser.readline().decode('utf-8')	# Read and print the received serial transmission
		print(recd_ack)
		
		if (recd_ack == ack_string + "\r\n"):	# Check if the recieved message is an acknowledgement message
			# print(ack_string + " received")
			break

# @brief: Configure the Serial port of the Omega board
# @par None
# @ret ser: Instantiation of Serial Port
def serial_port():
	ser = serial.Serial(
	    # port='/dev/ttyS1',\
        port='COM8',\
	    baudrate=9600,\
	    parity=serial.PARITY_NONE,\
	    stopbits=serial.STOPBITS_ONE,\
	    bytesize=serial.EIGHTBITS,\
	    timeout=None)
	print("Connected to: " + ser.portstr)
	return ser

# @brief: Configure the servo angle via the Serial port
# @par ser: The serial port instance
# @par angle: Servo angle
# @ret None
def servo_angle(ser, angle):
    send_command(ser, "COM_ANGLE")
    check_ack(ser, "ACK_ANGLE")
    send_command(ser, str(angle))
    check_ack(ser, "ACK_ANGLE")

# @brief: Set the position relative to the test point origin
# @par swift: The swift instance
# @par zero_position: The coordinates of the test point origin
# @par x_relative: X-coordinate relative to the test point origin
# @par y_relative: Y-coordinate relative to the test point origin
# @par z_relative: Z-coordinate relative to the test point origin
# @ret set_pos_status: Returns "OK" if coordinates are valid and returns "E22" if arm cannot execute command.
def position_relative_to_zero(swift, zero_position, x_relative, y_relative, z_relative):
    x_0 = zero_position[0]
    y_0 = zero_position[1]
    z_0 = zero_position[2]

    x_new = x_0 + x_relative
    y_new = y_0 + y_relative
    z_new = z_0 + z_relative

    set_pos_status = swift.set_position(x=x_new, y=y_new, z=z_new, wait=True)
    print("set_pos_status: ", set_pos_status)
    time.sleep(0.5)
    return set_pos_status


def main():
	# Set the arm mode and instantiate the Arduino serial port
	swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
	swift.waiting_ready()
	swift.set_mode(0)
	speed = 1000
	ser = serial_port()

	# Configure the test point origin coordinates
	x_0 = 114.8472 - 47.5
	y_0 = -13.9862 - 87.5
	z_0 = 50
	zero_position = [x_0, y_0, z_0]

	# Reset Motion
	servo_angle(ser, 90)
	time.sleep(1)
	swift.reset()
	servo_angle(ser, 0)

	# Move the arm to the center of the petri dish, turn the pump on and remove the lid.
	# Place the lid towards the side and turn the pump off.
	# 0,0 == [189.3567, 13.6758, 44.4596]
	swift.set_position(x=189+12.5, y=13.67-12.5, z=60)
	swift.set_pump(on=True)
	time.sleep(1.5)
	swift.set_position(x=189+12.5, y=13.67-12.5, z=100)
	swift.set_position(x=x_0, y=y_0, z=16)
	swift.set_pump(on=False)
	swift.reset()
	servo_angle(ser, 180)
	time.sleep(1)
	swift.set_buzzer(duration=1, wait=True)
	servo_angle(ser, 0)

	# Move the syringe to the desired location on the petri dish
	# Buzzer indicates syringe linear actuator movement.
	syringe_buzzer_duration = 0.1
	swift.set_position(x=189, y=13.67, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189, y=13.67-12.5, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189, y=13.67-25, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189+12.5, y=13.67, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189+12.5, y=13.67-12.5, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189+12.5, y=13.67-25, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189+25, y=13.67, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189+25, y=13.67-12.5, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)
	swift.set_position(x=189+25, y=13.67-25, z=60)
	swift.set_buzzer(duration=syringe_buzzer_duration, wait=True)

	# Pick and place the lid back on
	swift.reset()
	swift.set_position(x=x_0, y=y_0, z=15)
	swift.set_pump(on=True)
	swift.set_position(x=189+12.5, y=13.67-12.5, z=100)
	swift.set_position(x=189+12.5, y=13.67-12.5, z=60)
	time.sleep(1)
	swift.set_pump(on=False)


if __name__ == "__main__":
	main()