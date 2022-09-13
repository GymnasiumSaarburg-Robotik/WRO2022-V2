from pybricks.parameters import Stop
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
    diff = target + c.GYRO_SENSOR.angle()  # diff zwischen momentanem und target wert
    while diff > 3 or diff < -3:
        print(c.GYRO_SENSOR.angle)
        diff = c.GYRO_SENSOR.angle - target
        if diff < 0:
            c.DRIVING_MOTOR_LEFT.run(20)
            c.DRIVING_MOTOR_RIGHT.run(-20)
        else:
            c.DRIVING_MOTOR_LEFT.run(-20)
            c.DRIVING_MOTOR_RIGHT.run(20)
    c.DRIVING_MOTOR_LEFT.stop()
    c.DRIVING_MOTOR_RIGHT.stop()


def run_into_wall(angle) :
    while not c.PRESSURE_SENSOR.pressed():
        if c.GYRO_SENSOR.angle > angle:
            c.DRIVING_MOTOR_LEFT.run(speed=70)
            c.DRIVING_MOTOR_RIGHT.run(speed=100)
        else:
            c.DRIVING_MOTOR_LEFT.run(speed=100)
            c.DRIVING_MOTOR_RIGHT.run(speed=70)
    sleep(0.2)
    c.DRIVING_MOTOR_RIGHT.stop()
    c.DRIVING_MOTOR_LEFT.stop()

def face_outer_sleeping_pos_from_ramp():
    face_target(180)
    run_into_wall(180)
    c.DRIVING_MOTOR_LEFT.run_angle(-50, 72, then=Stop.BRAKE, wait=False)
    c.DRIVING_MOTOR_RIGHT.run_angle(-50, 72, then=Stop.BRAKE, wait=True)
    face_target(270)
    run_into_wall(270)


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
    c.DRIVING_MOTOR_LEFT.run_time(100, 0.5, Stop.BRAKE, False)
    c.DRIVING_MOTOR_RIGHT.run_time(100, 0.5, Stop.BRAKE, True)
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
    c.SECURING_MOTOR.run_time(50, 2, Stop.HOLD, True)
    c.SHOOTING_MOTOR.run_time(100, 1, Stop.BRAKE, True)
    c.SECURING_MOTOR.stop()
    c.SECURING_MOTOR.run_time(-50, 2, Stop.HOLD, True)
    c.SECURING_MOTOR.stop()



c = constants()
bm = basic_movement(c)

print("Waiting")
sleep(10)
shoot()
face_outer_sleeping_pos_from_ramp()
face_target(0)

