from serial import Serial

from uarm.wrapper import SwiftAPI
swift = SwiftAPI()

com = Serial("COM9", baudrate=115200)

print('getCD:', com.getCD())
print('getCTS:', com.getCTS())
print('getDSR:', com.getDSR())
print('getRI:', com.getRI())
print('get_settings:', com.get_settings())
print('timeout:', com.timeout)

