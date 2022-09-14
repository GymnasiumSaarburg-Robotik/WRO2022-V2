#!/usr/bin/env pybricks-micropython
from pybricks.iodevices import I2CDevice

from decryption.api import direction_data_new

from pybricks.parameters import Port, Stop
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, GyroSensor

from constants.constants import constants
from basic_movement.api import basic_movement


def face_ramp():
    print("Facing ramp...")
    target = 0  # plus entspricht uhrzeigersinn, minus entgegen Uhrzeigersinn
    diff = target + c.GYRO_SENSOR.angle  # diff zwischen momentanem und target wert
    while diff > 3 or diff < -3:
        print(c.GYRO_SENSOR.angle)
        diff = c.GYRO_SENSOR.angle - target
        if diff < 0:
            c.DRIVING_MOTOR_LEFT.run(10)
            c.DRIVING_MOTOR_RIGHT.run(-10)
        else:
            c.DRIVING_MOTOR_LEFT.run(-10)
            c.DRIVING_MOTOR_RIGHT.run(10)
    c.DRIVING_MOTOR_LEFT.stop()
    c.DRIVING_MOTOR_RIGHT.stop()


def only_contains_one_element(data):
    return len(set(data)) == 1


def shoot():
    blue = c.COLOR_SENSOR.rgb()[2]
    while blue > 140:
        blue = c.COLOR_SENSOR.rgb()[2]
        if c.GYRO_SENSOR.angle > 0:
            c.DRIVING_MOTOR_LEFT.run(speed=90)
            c.DRIVING_MOTOR_RIGHT.run(speed=100)
        else:
            c.DRIVING_MOTOR_LEFT.run(speed=90)
            c.DRIVING_MOTOR_RIGHT.run(speed=100)
    c.DRIVING_MOTOR_LEFT.on_for_seconds(100, 0.5, False, False)
    c.DRIVING_MOTOR_RIGHT.on_for_seconds(100, 0.5, False, True)
    blue = c.COLOR_SENSOR.rgb()[2]
    while blue > 200 or blue < 100:
        blue = c.COLOR_SENSOR.rgb()[2]
        if c.GYRO_SENSOR.angle > 0:
            c.DRIVING_MOTOR_LEFT.run(speed=45)
            c.DRIVING_MOTOR_RIGHT.run(speed=50)
        else:
            c.DRIVING_MOTOR_LEFT.run(speed=45)
            c.DRIVING_MOTOR_RIGHT.run(speed=50)
    c.DRIVING_MOTOR_LEFT.stop()
    c.DRIVING_MOTOR_RIGHT.stop()
    c.SECURING_MOTOR.run_time(100, 1, Stop.BRAKE, True)
    c.SHOOTING_MOTOR.run_time(100, 0.5, Stop.BRAKE, True)


def move_towards_sleeping_pos1():  # pos 1 describse the sleeping pos for a robot coming from shooting process
    c.DRIVING_MOTOR_LEFT.run_time(100, 5, Stop.BRAKE, False)
    c.DRIVING_MOTOR_RIGHT.run_time(100, 5, Stop.BRAKE, True)


def readBlocks(current_direction):
    device = I2CDevice(Port.S1, c.CAMERA_ADDRESS)
    data = [174, 193, 32, 2, 255, 255]
    device.write(174, bytes(data))
    # Read first block
    data = ""
    block = list(device.read(0, 6 + 14))
    print(str(block))
    if not only_contains_one_element(block[7:]):
        data += str(block)
    while True:
        block2 = list(device.read(0, 14))
        if only_contains_one_element(block2):
            break
        data += "|\n" + str(block2)
    return direction_data_new(data, current_direction)


c = constants()
bm = basic_movement(c)

c.GYRO_SENSOR.reset_angle(0)
print("init: " + str(c.GYRO_SENSOR.angle))
chasingBall = False

while True:

    # New approach: No direct line, rather alignment on two seperate dimensions

    direction_data = readBlocks(c.GYRO_SENSOR.angle())
    relative_positions_raw = direction_data.relativeDirections
    print("Count:" + str(len(relative_positions_raw)))
    relative_positions = [round(num, 0) for num in relative_positions_raw]
    # values between 0 and 1; < 0.5 left hand side; > 0.5 right
    rel = relative_positions[0]

    if rel > 0.5:
        pass
        # Turn, drive abs(rel)/0.5 * MAX_DISTANCE
    else:
        pass
        # Turn other direction, drive ''

    # face_ramp
    # drive an estimated distance

print("Done")
sleep(30)
