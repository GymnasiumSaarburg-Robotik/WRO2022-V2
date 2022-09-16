
from pybricks.parameters import Port
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, GyroSensor

class constants:

    def __init__(self):
        pass
        self.DRIVING_MOTOR_LEFT = Motor(Port.B)  # motor 1
        self.DRIVING_MOTOR_RIGHT = Motor(Port.C)  # motor 2
        self.SECURING_MOTOR = Motor(Port.A)
        self.SHOOTING_MOTOR = Motor(Port.D)

        self.PRESSURE_SENSOR = TouchSensor(Port.S4)
        self.GYRO_SENSOR = GyroSensor(Port.S3)
        self.GYRO_SENSOR.reset_angle(0)
        self.COLOR_SENSOR = ColorSensor(Port.S2)

        self.CAMERA_ADDRESS = 0x54
        #input1 = LegoPort(Port.S1)
        #input1.mode = 'other-i2c'
        #self.BUS = SMBus(3)
