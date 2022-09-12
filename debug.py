from smbus import SMBus
from ev3dev2.display import *
from ev3dev2.sensor import *
from ev3dev2.port import LegoPort
from ev3dev2.motor import *

from decryption.api import direction_data_new

from time import *

from constants.constants import constants
from basic_movement.api import basic_movement



def face_target(target):
    print("Facing ramp...")  # plus entspricht uhrzeigersinn, minus entgegen Uhrzeigersinn
    diff = target + c.GYRO_SENSOR.angle  # diff zwischen momentanem und target wert
    while diff > 3 or diff < -3:
        print(c.GYRO_SENSOR.angle)
        diff = c.GYRO_SENSOR.angle - target
        if diff < 0:
            c.DRIVING_MOTOR_LEFT.on(20)
            c.DRIVING_MOTOR_RIGHT.on(-20)
        else:
            c.DRIVING_MOTOR_LEFT.on(-20)
            c.DRIVING_MOTOR_RIGHT.on(20)
    c.DRIVING_MOTOR_LEFT.off()
    c.DRIVING_MOTOR_RIGHT.off()


def run_into_wall(angle) :
    while not c.PRESSURE_SENSOR.is_pressed:
        if c.GYRO_SENSOR.angle > angle:
            c.DRIVING_MOTOR_LEFT.on(speed=70)
            c.DRIVING_MOTOR_RIGHT.on(speed=100)
        else:
            c.DRIVING_MOTOR_LEFT.on(speed=100)
            c.DRIVING_MOTOR_RIGHT.on(speed=70)
    sleep(0.2)
    c.DRIVING_MOTOR_RIGHT.off()
    c.DRIVING_MOTOR_LEFT.off()

def face_outer_sleeping_pos_from_ramp():
    face_target(180)
    run_into_wall(180)
    c.DRIVING_MOTOR_LEFT.on_for_rotations(speed=-50, rotations=0.2, block=False)
    c.DRIVING_MOTOR_RIGHT.on_for_rotations(speed=-50, rotations=0.2)
    face_target(270)
    run_into_wall(270)


def shoot():
    blue = c.COLOR_SENSOR.rgb[2]
    while blue > 140:
        blue = c.COLOR_SENSOR.rgb[2]
        if c.GYRO_SENSOR.angle > 0:
            c.DRIVING_MOTOR_LEFT.on(speed=90)
            c.DRIVING_MOTOR_RIGHT.on(speed=100)
        else:
            c.DRIVING_MOTOR_LEFT.on(speed=90)
            c.DRIVING_MOTOR_RIGHT.on(speed=100)
    c.DRIVING_MOTOR_LEFT.on_for_seconds(100, 0.5, False, False)
    c.DRIVING_MOTOR_RIGHT.on_for_seconds(100, 0.5, False, True)
    blue = c.COLOR_SENSOR.rgb[2]
    while blue > 200 or blue < 100:
        blue = c.COLOR_SENSOR.rgb[2]
        if c.GYRO_SENSOR.angle > 0:
            c.DRIVING_MOTOR_LEFT.on(speed=45)
            c.DRIVING_MOTOR_RIGHT.on(speed=50)
        else:
            c.DRIVING_MOTOR_LEFT.on(speed=45)
            c.DRIVING_MOTOR_RIGHT.on(speed=50)
    c.DRIVING_MOTOR_LEFT.off()
    c.DRIVING_MOTOR_RIGHT.off()
    c.SECURING_MOTOR.on_for_seconds(50, 2, True, True)
    c.SHOOTING_MOTOR.on_for_seconds(100, 1, False, True)
    c.SECURING_MOTOR.off(brake=False)
    c.SECURING_MOTOR.on_for_seconds(-50, 2, True, True)
    c.SECURING_MOTOR.off(False)



c = constants()
bm = basic_movement(c)

print("Waiting")
sleep(10)
shoot()
face_outer_sleeping_pos_from_ramp()
face_target(0)

