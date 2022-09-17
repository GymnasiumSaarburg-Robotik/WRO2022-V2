import re
from time import sleep

from pybricks.parameters import Stop


class basic_movement:

    def __init__(self, constants_instance):
        self.c = constants_instance

    # Wall interaction

    def run_into_wall(self):
        while not self.c.PRESSURE_SENSOR.pressed():
            self.c.DRIVING_MOTOR_LEFT.run(speed=500)
            self.c.DRIVING_MOTOR_RIGHT.run(speed=500)
        sleep(0.2)
        self.c.DRIVING_MOTOR_RIGHT.hold()
        self.c.DRIVING_MOTOR_LEFT.hold()

    def run_into_wall_angle(self, angle):
        while not self.c.PRESSURE_SENSOR.pressed():
            if self.c.GYRO_SENSOR.angle() < angle:
                self.c.DRIVING_MOTOR_LEFT.run(speed=800)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=1000)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(speed=1000)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=800)
        sleep(0.2)
        self.c.DRIVING_MOTOR_RIGHT.hold()
        self.c.DRIVING_MOTOR_LEFT.hold()

    # Cage

    def open_cage(self):  # Moving the cage out of the hovering position up to its upper max
        self.c.SECURING_MOTOR.run_time(10000, 1300, Stop.HOLD, True)

    def close_cage(self):  # Moving the cage down from its upper MAX down to floor level \n centering it afterwards
        self.c.SECURING_MOTOR.run_time(-400, 1500, Stop.HOLD, True)
        self.center_cage()

    def center_cage(self):  # Moving the cage from ground up to its target position
        self.c.SECURING_MOTOR.run_time(675, self.c.CAGE_CENTER_DURATION, Stop.HOLD, True)

    # Driving

    def drive(self, speed, rotations):
        self.c.DRIVING_MOTOR_LEFT.run_angle(speed, rotations * 360, Stop.BRAKE, False)
        self.c.DRIVING_MOTOR_RIGHT.run_angle(speed, rotations * 360, Stop.BRAKE, True)

    def drive_rotations(self, rotations):
        self.c.DRIVING_MOTOR_LEFT.reset_angle(0)
        while self.c.DRIVING_MOTOR_LEFT.angle() < rotations:
            if self.c.GYRO_SENSOR.angle() < 0:
                self.c.DRIVING_MOTOR_LEFT.run(speed=300)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=250)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(speed=250)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=300)

    def drive_rotations_target(self, rotations, angle=0):
        self.c.DRIVING_MOTOR_LEFT.reset_angle(0)
        while self.c.DRIVING_MOTOR_LEFT.angle() < rotations:
            if self.c.GYRO_SENSOR.angle() < angle:
                self.c.DRIVING_MOTOR_LEFT.run(speed=450)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=400)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(speed=400)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=450)

    # Orientation

    def face_target(self, target):
        diff = target + self.c.GYRO_SENSOR.angle()
        while diff > 1 or diff < -1:
            diff = self.c.GYRO_SENSOR.angle() - target
            if diff < 0:
                self.c.DRIVING_MOTOR_LEFT.run(150)
                self.c.DRIVING_MOTOR_RIGHT.run(-150)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(-150)
                self.c.DRIVING_MOTOR_RIGHT.run(150)
        self.c.DRIVING_MOTOR_LEFT.hold()
        self.c.DRIVING_MOTOR_RIGHT.hold()
