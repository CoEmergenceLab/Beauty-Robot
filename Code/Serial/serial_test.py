import serial
import time

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

# @brief: Send X/Y/Z coordinates over serial
# @par ser: Instantiation of Serial Port
# @par nval: X/Y/Z coordinates
# @ret None
def xsend(ser, xval):
    send_command(ser, "COM_X")
    check_ack(ser, "ACK_X")
    send_command(ser, str(xval))
    check_ack(ser, "ACK_X")

def ysend(ser, yval):
    send_command(ser, "COM_Y")
    check_ack(ser, "ACK_Y")
    send_command(ser, str(yval))
    check_ack(ser, "ACK_Y")

def zsend(ser, zval):
    send_command(ser, "COM_Z")
    check_ack(ser, "ACK_Z")
    send_command(ser, str(zval))
    check_ack(ser, "ACK_Z")

# @brief: Send all three dimensions -- X, Y, Z coordinates over serial
# @par ser: Instantiation of Serial Port
# @par xval: X-coordinates
# @par yval: Y-coordinates
# @par zval: Z-coordinates
# @ret None
def send_coordinates(ser, xval, yval, zval):
    xsend(ser, xval)
    ysend(ser, yval)
    zsend(ser, zval)

def main():
    xval = 1
    yval = 2
    zval = 3
    ser = serial_port()
    while(1):
        print("Retrieving latest volcano data")
        send_coordinates(ser, xval, yval, zval)
        
if __name__ == "__main__":
    main()
