from dual_motor_controller import DualMotorController
from gpiozero import Motor


class SmartCarMotorController(DualMotorController):
    def __init__(self):
        super(SmartCarMotorController, self).__init__()
        self._left_motor = Motor(4, 14)
        self._right_motor = Motor(18, 17)

    def set_speeds(self, speed_left, speed_right):
        print(str(speed_left), str(speed_right))
        if speed_left < 0:
            self._left_motor.backward(-speed_left)
        else:
            self._left_motor.forward(speed_left)
        if speed_right < 0:
            self._right_motor.backward(-speed_right)
        else:
            self._right_motor.forward(speed_right)
