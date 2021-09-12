'''
Assuming Z operates in only the positive axis and z_min is at 5
For z=5, y=0: x_min=84, x_max=359
For z=5, x=84: y_min=-349, y_max=349 
For x=84, y=-349: z_min=-2, z_max=68 

'''

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})

swift.waiting_ready()

'''
Reset the uArm position to 200, 0, 150.
Set arm to normal mode
'''
swift.reset(wait=True)
swift.set_mode(0)
speed = 100000

swift.set_buzzer(1000, 0.5)

x_min = 0
x_max = 0
y_min = 0
y_max = 0
z_min = 0
z_max = 0
prev_ret = 0

# Test X-range
for i in range(-500, 500):
    ret_set_pos_status = swift.set_position(x=i, y=0, z=5, speed=speed, wait=True)
    # print("x: " + str(i) + "   ret: " + ret_set_pos_status)
    if prev_ret  == "E22":
        if ret_set_pos_status == "OK":
            x_min = i
    if ret_set_pos_status == "OK":
        x_max = i
    prev_ret = ret_set_pos_status    
print("X Max/Min: " + str(x_max) + " / " + str(x_min))

#Test Y-range
swift.reset(wait=True)
swift.set_buzzer(1000, 0.5)
for i in range(-500, 500):
    ret_set_pos_status = swift.set_position(x=x_min, y=i, z=5, speed=speed, wait=True)
    # print("y: " + str(i) + "   ret: " + ret_set_pos_status)
    if prev_ret  == "E22":
        if ret_set_pos_status == "OK":
            y_min = i
    if ret_set_pos_status == "OK":
        y_max = i
    prev_ret = ret_set_pos_status    
print("Y Max/Min: " + str(y_max) + " / " + str(y_min))

# Test Z-range 
swift.reset(wait=True)
swift.set_buzzer(1000, 0.5)
for i in range(-500, 500):
    ret_set_pos_status = swift.set_position(x=x_min, y=y_min, z=i, speed=speed, wait=True)
    # print("z: " + str(i) + "   ret: " + ret_set_pos_status)
    if prev_ret  == "E22":
        if ret_set_pos_status == "OK":
            z_min = i
    if ret_set_pos_status == "OK":
        z_max = i
    prev_ret = ret_set_pos_status    
print("Z Max/Min: " + str(z_max) + " / " + str(z_min))

# Test Z-range for Y=0
swift.reset(wait=True)
swift.set_buzzer(1000, 0.5)
for i in range(-500, 500):
    ret_set_pos_status = swift.set_position(x=87, y=0, z=i, speed=speed, wait=True)
    # print("z: " + str(i) + "   ret: " + ret_set_pos_status)
    if prev_ret  == "E22":
        if ret_set_pos_status == "OK":
            z_min = i
    if ret_set_pos_status == "OK":
        z_max = i
    prev_ret = ret_set_pos_status    
print("X=84, Y=0, Z Max/Min: " + str(z_max) + " / " + str(z_min))

swift.reset(wait=True)
swift.set_buzzer(1000, 0.5)
for i in range(-500, 500):
    ret_set_pos_status = swift.set_position(x=359, y=0, z=i, speed=speed, wait=True)
    # print("z: " + str(i) + "   ret: " + ret_set_pos_status)
    if prev_ret  == "E22":
        if ret_set_pos_status == "OK":
            z_min = i
    if ret_set_pos_status == "OK":
        z_max = i
    prev_ret = ret_set_pos_status    
print("X=359, Y=0, Z Max/Min: " + str(z_max) + " / " + str(z_min))



time.sleep(4)
swift.flush_cmd()
swift.disconnect()