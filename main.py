#!/usr/bin/env pybricks-micropython

from pybricks.iodevices import I2CDevice

from decryption.api import direction_data_new

from time import *

from pybricks.parameters import Port, Stop
from pybricks.ev3devices import Motor

from constants.constants import constants
from basic_movement.api import basic_movement
from messaging.messaging_client import messaging_client
from messaging.messaging_server import messaging_server


def only_contains_one_element(data):
    return len(set(data)) == 1


def shoot():
    blue = c.COLOR_SENSOR.rgb()[2]
    print("Blue: " + str(blue))
    while blue > 50:
        blue = c.COLOR_SENSOR.rgb()[2]
        if c.GYRO_SENSOR.angle() < 0:
            c.DRIVING_MOTOR_LEFT.run(speed=400)
            c.DRIVING_MOTOR_RIGHT.run(speed=370)
        else:
            c.DRIVING_MOTOR_LEFT.run(speed=370)
            c.DRIVING_MOTOR_RIGHT.run(speed=400)
    c.DRIVING_MOTOR_LEFT.run_time(500, 1000, Stop.BRAKE, False)
    c.DRIVING_MOTOR_RIGHT.run_time(500, 1000, Stop.BRAKE, True)
    blue = c.COLOR_SENSOR.rgb()[2]
    while blue > 250 or blue < 40:
        blue = c.COLOR_SENSOR.rgb()[2]
        print(str(blue))
        if c.GYRO_SENSOR.angle() < 0:
            c.DRIVING_MOTOR_LEFT.run(speed=300)
            c.DRIVING_MOTOR_RIGHT.run(speed=250)
        else:
            c.DRIVING_MOTOR_LEFT.run(speed=250)
            c.DRIVING_MOTOR_RIGHT.run(speed=300)
    c.DRIVING_MOTOR_LEFT.stop()
    c.DRIVING_MOTOR_RIGHT.stop()
    bm.open_cage()
    c.SHOOTING_MOTOR.run_angle(3000, 360, Stop.BRAKE, True)
    bm.close_cage()


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
    if not only_contains_one_element(block[7:]):
        data += str(block)
    while True:
        block2 = list(device.read(0, 14))
        if only_contains_one_element(block2):
            break
        data += "|\n" + str(block2)
    return direction_data_new(data, current_direction)

def rotations_to_nearest_ball():
    # New approach: No direct line, rather alignment on two seperate dimensions
    array = [None] * 30
    for i in range(30):
        direction_data = readBlocks(c.GYRO_SENSOR.angle())
        if len(direction_data.blocks) == 0:
            continue
        size = direction_data.blocks[0].size
        dist = 2000.5 * pow(size, -0.651)
        array[i] = dist

    distance = 0
    for a in range(30):
        if array[a] is None:
            continue
        distance += array[a]
    distance = distance / 30
    return distance / 15 + 1.5

def grab_ball():
    direction_data = readBlocks(c.GYRO_SENSOR.angle())
    relative_positions_raw = direction_data.relativeDirections
    relative_positions = [round(num, 2) for num in relative_positions_raw]

    rel = relative_positions[0]
    if rel > 0.55:
        bm.face_target(90)
    elif rel < 0.45:
        bm.face_target(-90)
    sleep(0.1)

    rel2 = abs(0.5 - rel)
    if rel < 0.15:
        bm.run_into_wall_angle(-90)
        bm.drive(-120, 0.1)
        bm.face_target(-5)
        rotations = rotations_to_nearest_ball()
        bm.open_cage()
        bm.drive_rotations_target(rotations * 360, -5)
    elif rel2 != 0.5:
        c.DRIVING_MOTOR_LEFT.run_time(720, rel2 * 3.5 * 1100, Stop.BRAKE, False)
        c.DRIVING_MOTOR_RIGHT.run_time(720, rel2 * 3.5 * 1100, Stop.BRAKE, True)
        bm.face_target(0)
        rotations = rotations_to_nearest_ball()
        bm.open_cage()
        bm.drive_rotations(rotations * 360)

    bm.close_cage_async()
    bm.drive(180, 0.25)

def leave_left_start_pos():
    messaging.send(2)
    bm.drive(180, 0.2)
    bm.face_target(-90)

def leave_right_start_pos():
    messaging.send(0)
    bm.drive(180, 0.2)
    bm.face_target(-90)
    messaging.wait_for_zone0(True)


c = constants()
bm = basic_movement(c)
messaging = messaging_server()

bm.close_cage()
bm.center_cage()

if isinstance(messaging, messaging_server): # bot starting on the left position
    leave_left_start_pos()
elif isinstance(messaging, messaging_client): # bot starting ob the right position
    leave_right_start_pos()
while True:
    bm.run_into_wall()
    c.GYRO_SENSOR.reset_angle(-90)
    bm.drive(-240, 1.8)
    bm.face_target(0)

    # pick up ball
    messaging.ev3.speaker.beep(100, 2000)

    bm.run_into_wall_angle(0)
    c.GYRO_SENSOR.reset_angle(0)
    bm.drive(-180, 0.2)
    bm.face_target(90)
    bm.run_into_wall_angle(90)
    c.GYRO_SENSOR.reset_angle(90)
    bm.drive(-180, 0.2)

    bm.face_target(180)
    bm.drive_rotations_target(5.8 * 360, 180)
    bm.face_target(90)
    bm.drive_rotations_target(3.7 * 360, 90)
    bm.face_target(0)
    shoot()
    bm.drive(-180, 3)
    bm.face_target(-180)
    sleep(0.5)
    bm.run_into_wall()
    c.GYRO_SENSOR.reset_angle(-180)
    bm.drive(-180, 0.5)
    bm.face_target(-90)
    sleep(5)
