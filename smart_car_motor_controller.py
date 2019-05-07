from motor_controller import MotorController
from gpiozero import Motor


class SmartCarMotorController(MotorController):
    def __init__(self):
        self.__left_motor = Motor(4, 14)
        self.__right_motor = Motor(18, 17)

    def set_speeds(self, speed_left, speed_right):
        if speed_left < 0:
            self.__left_motor.backward(speed_left)
        else:
            self.__left_motor.forward(speed_left)
        if speed_right < 0:
            self.__right_motor.backward(speed_right)
        else:
            self.__right_motor.forward(speed_right)
