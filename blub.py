#!/usr/bin/env pybricks-micropython

from pybricks.iodevices import I2CDevice
from smbus import SMBus
from ev3dev2.display import *
from ev3dev2.sensor import *
from ev3dev2.port import LegoPort
from ev3dev2.motor import *

from decryption.api import direction_data_new

from time import *

from constants.constants import constants
from basic_movement.api import basic_movement


def only_contains_one_element(data):
    return len(set(data)) == 1

def readBlocks(current_direction):
    device = I2CDevice(INPUT_2, c.CAMERA_ADDRESS)
    data = [174, 193, 32, 2, 255, 255]
    device.write(None, data)
    # Read first block
    data = ""
    block = device.read(0, 6 + 14)
    if not only_contains_one_element(block[7:]):
        data += str(block)
    while True:
        block2 = device.read(0, 14)
        if only_contains_one_element(block2):
            break
        data += "|\n" + str(block2)
    return direction_data_new(data, current_direction)


c = constants()
bm = basic_movement(c)

#c.GYRO_SENSOR.reset_angle(0)
#print("init: " + str(c.GYRO_SENSOR.angle))
#chasingBall = False

# New approach: No direct line, rather alignment on two seperate dimensions

direction_data = readBlocks(0)
relative_positions_raw = direction_data.relativeDirections
print("Count:" + str(len(relative_positions_raw)))

print("Done")
sleep(30)
