import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI


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
    swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})

    swift.waiting_ready()

    swift.set_mode(0)
    speed = 1000

    # Get the initial position of the arm.
    position = swift.get_position(wait=True)
    print(position)

    # Test point origin coordinates(0,0)

    # x_0 = 114.8472 - 47.5
    # y_0 = -13.9862 - 87.5
    # z_0 = 10
    x_0 = 66
    y_0 = -100
    z_0 = 10

    zero_position = [x_0, y_0, z_0]

    # Move arm to Origin and center of test jig
    swift.set_buzzer(1000, 0.5)
    set_pos_status = swift.set_position(x=x_0, y=y_0, z=z_0, speed=speed, wait=True)
    print("set_pos_status: ", set_pos_status)
    time.sleep(2)

    position_relative_to_zero(swift, zero_position, 100, 100, 0)

    # Move arm to all test points on the jig
    position_relative_to_zero(swift, zero_position, 62.5, 12.5, 0)
    position_relative_to_zero(swift, zero_position, 87.5, 12.5, 0)
    position_relative_to_zero(swift, zero_position, 112.5, 12.5, 0)
    position_relative_to_zero(swift, zero_position, 137.5, 12.5, 0)

    position_relative_to_zero(swift, zero_position, 62.5, 37.5, 0)
    position_relative_to_zero(swift, zero_position, 87.5, 37.5, 0)
    position_relative_to_zero(swift, zero_position, 112.5, 37.5, 0)
    position_relative_to_zero(swift, zero_position, 137.5, 37.5, 0)

    position_relative_to_zero(swift, zero_position, 12.5, 62.5, 0)
    position_relative_to_zero(swift, zero_position, 37.5, 62.5, 0)
    position_relative_to_zero(swift, zero_position, 87.5, 62.5, 0)
    position_relative_to_zero(swift, zero_position, 112.5, 62.5, 0)
    position_relative_to_zero(swift, zero_position, 162.5, 62.5, 0)
    position_relative_to_zero(swift, zero_position, 187.5, 62.5, 0)

    position_relative_to_zero(swift, zero_position, 12.5, 87.5, 0)
    position_relative_to_zero(swift, zero_position, 37.5, 87.5, 0)
    position_relative_to_zero(swift, zero_position, 62.5, 87.5, 0)
    position_relative_to_zero(swift, zero_position, 137.5, 87.5, 0)
    position_relative_to_zero(swift, zero_position, 162.5, 87.5, 0)
    position_relative_to_zero(swift, zero_position, 187.5, 87.5, 0)

    position_relative_to_zero(swift, zero_position, 12.5, 112.5, 0)
    position_relative_to_zero(swift, zero_position, 37.5, 112.5, 0)
    position_relative_to_zero(swift, zero_position, 62.5, 112.5, 0)
    position_relative_to_zero(swift, zero_position, 137.5, 112.5, 0)
    position_relative_to_zero(swift, zero_position, 162.5, 112.5, 0)
    position_relative_to_zero(swift, zero_position, 187.5, 112.5, 0)

    position_relative_to_zero(swift, zero_position, 12.5, 137.5, 0)
    position_relative_to_zero(swift, zero_position, 37.5, 137.5, 0)
    position_relative_to_zero(swift, zero_position, 87.5, 137.5, 0)
    position_relative_to_zero(swift, zero_position, 112.5, 137.5, 0)
    position_relative_to_zero(swift, zero_position, 162.5, 137.5, 0)
    position_relative_to_zero(swift, zero_position, 187.5, 137.5, 0)

    position_relative_to_zero(swift, zero_position, 62.5, 162.5, 0)
    position_relative_to_zero(swift, zero_position, 87.5, 162.5, 0)
    position_relative_to_zero(swift, zero_position, 112.5, 162.5, 0)
    position_relative_to_zero(swift, zero_position, 137.5, 162.5, 0)

    position_relative_to_zero(swift, zero_position, 62.5, 187.5, 0)
    position_relative_to_zero(swift, zero_position, 87.5, 187.5, 0)
    position_relative_to_zero(swift, zero_position, 112.5, 187.5, 0)
    position_relative_to_zero(swift, zero_position, 137.5, 187.5, 0)


if __name__ == "__main__":
    main()
