import re
from time import sleep

from pybricks.parameters import Stop

from constants.constants import constants
from decryption.block import CCblock


class basic_movement:

    def __init__(self, constants_instance):
        self.c = constants_instance

    def run_into_wall(self, angle):
        while not self.c.PRESSURE_SENSOR.pressed():
            print(str(self.c.GYRO_SENSOR.angle()))
            if self.c.GYRO_SENSOR.angle() > angle:
                self.c.DRIVING_MOTOR_LEFT.run(speed=720)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=1000)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(speed=1000)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=720)
        sleep(0.2)
        self.c.DRIVING_MOTOR_RIGHT.hold()
        self.c.DRIVING_MOTOR_LEFT.hold()

    def move_towards_sleeping_pos1(self, current_direction):
        pass


    def move_towards_sleeping_pos2(self, current_direction):
        pass

    def open_cage(self):
        self.c.SECURING_MOTOR.run_time(5000, 2000, Stop.HOLD, True)
        pass

    def close_cage_async(self):
        self.c.SECURING_MOTOR.run_time(-400, 2000, Stop.BRAKE, False)
        pass

    def drive(self, speed, rotations):
        self.c.DRIVING_MOTOR_LEFT.run_angle(speed, rotations * 360, Stop.BRAKE, False)
        self.c.DRIVING_MOTOR_RIGHT.run_angle(speed, rotations * 360, Stop.BRAKE, True)

    def drive_rotations(self, angle):
        self.c.DRIVING_MOTOR_LEFT.reset_angle(0)
        while self.c.DRIVING_MOTOR_LEFT.angle() < angle:
            if self.c.GYRO_SENSOR.angle() < 0:
                self.c.DRIVING_MOTOR_LEFT.run(speed=300)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=250)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(speed=250)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=300)


    def drive_rotations_target(self, angle, target):
        self.c.DRIVING_MOTOR_LEFT.reset_angle(0)
        while self.c.DRIVING_MOTOR_LEFT.angle() < angle:
            if self.c.GYRO_SENSOR.angle() < target:
                self.c.DRIVING_MOTOR_LEFT.run(speed=300)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=250)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(speed=250)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=300)

    def face_target(self, target):
        diff = target + self.c.GYRO_SENSOR.angle()  # diff zwischen momentanem und target wert
        while diff > 1 or diff < 1:
            print(str(self.c.GYRO_SENSOR.angle()))
            diff = self.c.GYRO_SENSOR.angle() - target
            if diff < 0:
                self.c.DRIVING_MOTOR_LEFT.run(150)
                self.c.DRIVING_MOTOR_RIGHT.run(-150)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(-150)
                self.c.DRIVING_MOTOR_RIGHT.run(150)
        self.c.DRIVING_MOTOR_LEFT.hold()
        self.c.DRIVING_MOTOR_RIGHT.hold()
        print(str(self.c.GYRO_SENSOR.angle()))