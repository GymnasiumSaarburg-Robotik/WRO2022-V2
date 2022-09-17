#!/usr/bin/env pybricks-micropython

from time import *

from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port, Stop

from basic_movement.api import basic_movement
from constants.constants import constants
from decryption.api import direction_data_new
from messaging.messaging_client import messaging_client
from messaging.messaging_server import messaging_server
from pybricks.hubs import EV3Brick


def only_contains_one_element(data):
    return len(set(data)) == 1


def shoot():
    blue = c.COLOR_SENSOR.rgb()[2]
    while blue > c.MIN_BLUE_ON_WHITE:  # Weißer Untergrund -> Hoher Blau wert
        blue = c.COLOR_SENSOR.rgb()[2]
        if c.GYRO_SENSOR.angle() < 0:
            c.DRIVING_MOTOR_LEFT.run(speed=400)
            c.DRIVING_MOTOR_RIGHT.run(speed=370)
        else:
            c.DRIVING_MOTOR_LEFT.run(speed=370)
            c.DRIVING_MOTOR_RIGHT.run(speed=400)
    c.DRIVING_MOTOR_LEFT.run_time(600, 1200, Stop.BRAKE, False)
    c.DRIVING_MOTOR_RIGHT.run_time(600, 1200, Stop.BRAKE, True)
    blue = c.COLOR_SENSOR.rgb()[2]
    while blue < c.MAX_BLUE_ON_GREEN:  # Grüner Untergrund -> Niedriger Blau wert
        blue = c.COLOR_SENSOR.rgb()[2]
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


def readBlocks():
    device = I2CDevice(Port.S1, c.CAMERA_ADDRESS)
    data = [174, 193, 32, 2, 255, 255]
    try:
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
    except True:
        return None
    return direction_data_new(data)


def rotations_to_nearest_ball():
    # New approach: No direct line, rather alignment on two seperate dimensions
    array = [None] * 30
    for i in range(30):
        direction_data = readBlocks()
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

    balls_found = False

    for i in range(2):
        sleep(3)
        direction_data = readBlocks()
        if direction_data == None:
            continue
        relative_positions_raw = direction_data.relativeDirections
        relative_positions = [round(num, 2) for num in relative_positions_raw]
        if (len(relative_positions) > 0) :
            balls_found = True
            break
    if (balls_found):
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
            c.DRIVING_MOTOR_LEFT.run_time(720, rel2 * 3.2 * 1100, Stop.BRAKE, False)
            c.DRIVING_MOTOR_RIGHT.run_time(720, rel2 * 3.2 * 1100, Stop.BRAKE, True)
            c.DRIVING_MOTOR_LEFT.hold()
            c.DRIVING_MOTOR_RIGHT.hold()
            bm.face_target(0)
            rotations = rotations_to_nearest_ball()
            bm.open_cage()
            bm.drive_rotations(rotations * 360)
        bm.close_cage()
        c.DRIVING_MOTOR_LEFT.hold()
        c.DRIVING_MOTOR_RIGHT.hold()


def leave_left_start_pos():
    messaging.send(2)
    bm.drive(180, 0.2)
    bm.face_target(-90)


def leave_right_start_pos():
    bm.drive(180, 0.2)
    bm.face_target(-90)

ev3 = EV3Brick()
c = constants()
bm = basic_movement(c)
messaging = messaging_server()

while True:
    if len(ev3.buttons.pressed()) > 0:
        break

c.GYRO_SENSOR.reset_angle(0)
bm.close_cage()

if isinstance(messaging, messaging_server):  # server-bot starting on the left position
    sleep(22)
    leave_left_start_pos()
elif isinstance(messaging, messaging_client):  # client-bot starting ob the right position
    leave_right_start_pos()

while True:
    bm.run_into_wall()
    c.GYRO_SENSOR.reset_angle(-90)
    bm.drive(-240, 1.8)
    bm.face_target(0)
    sleep(0.2)
    # pick up ball
    grab_ball()
    sleep(0.2)
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
 