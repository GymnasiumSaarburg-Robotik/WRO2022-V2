import re
from time import sleep

from pybricks.parameters import Stop


class basic_movement:

    def __init__(self, constants_instance):
        self.c = constants_instance

    def run_into_wall(self):
        while not self.c.PRESSURE_SENSOR.pressed():
            self.c.DRIVING_MOTOR_LEFT.run(speed=500)
            self.c.DRIVING_MOTOR_RIGHT.run(speed=500)
        sleep(0.2)
        self.c.DRIVING_MOTOR_RIGHT.hold()
        self.c.DRIVING_MOTOR_LEFT.hold()

    def run_into_wall_angle(self, angle):
        while not self.c.PRESSURE_SENSOR.pressed():
            print(str(self.c.GYRO_SENSOR.angle()))
            if self.c.GYRO_SENSOR.angle() < angle:
                self.c.DRIVING_MOTOR_LEFT.run(speed=800)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=1000)
            else:
                self.c.DRIVING_MOTOR_LEFT.run(speed=1000)
                self.c.DRIVING_MOTOR_RIGHT.run(speed=800)
        sleep(0.2)
        self.c.DRIVING_MOTOR_RIGHT.hold()
        self.c.DRIVING_MOTOR_LEFT.hold()

    def move_towards_sleeping_pos1(self, current_direction):
        pass

    def move_towards_sleeping_pos2(self, current_direction):
        pass

    # Cage

    def open_cage(self):
        self.c.SECURING_MOTOR.run_time(5000, 1000, Stop.HOLD, True)
        pass

    def close_cage_async(self):
        self.c.SECURING_MOTOR.run_time(-400, 2000, Stop.BRAKE, False)
        pass

    def close_cage(self):
        self.c.SECURING_MOTOR.run_time(-300, 250, Stop.HOLD, True)
        pass

    def center_cage(self):
        self.c.SECURING_MOTOR.run_time(300, self.c.CAGE_CENTER_DURATION, Stop.HOLD, True)
        pass
    center_cage().__doc__ = "Moving the cage from ground up to its target position"

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
        while diff > 0 or diff < 0:
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
