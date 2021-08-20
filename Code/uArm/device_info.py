import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})

swift.waiting_ready()

device_info = swift.get_device_info()
device_type  = device_info['device_type']
hardware_version  = device_info['hardware_version']
firmware_version  = device_info['firmware_version']
api_version  = device_info['api_version']
device_unique  = device_info['device_unique']
print("Device Type: ", device_type)
print("H/W Version: ", hardware_version)
print("F/W Version: ", firmware_version)
print("API Version: ", api_version)
print("Device Unique: ", device_unique)

power_status = swift.get_power_status()
print("Power Status: ", power_status)


swift.flush_cmd()
swift.disconnect