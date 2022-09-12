
from pybricks.parameters import Port
from pybricks.ev3devices import Motor

class constants:

    def __init__(self):
        pass
       # self.DRIVING_MOTOR_LEFT = LargeMotor(OUTPUT_B)  # motor 1
       # self.DRIVING_MOTOR_RIGHT = LargeMotor(OUTPUT_C)  # motor 2
       # self.SECURING_MOTOR = MediumMotor(OUTPUT_A)
       # self.SHOOTING_MOTOR = MediumMotor(OUTPUT_D)

       # self.PRESSURE_SENSOR = TouchSensor(INPUT_4)
       # self.GYRO_SENSOR = GyroSensor(INPUT_3)
       # self.GYRO_SENSOR.calibrate()
       # self.COLOR_SENSOR = ColorSensor(INPUT_2)

        self.CAMERA_ADDRESS = 0x54
        #input1 = LegoPort(Port.S1)
        #input1.mode = 'other-i2c'
        #self.BUS = SMBus(3)
