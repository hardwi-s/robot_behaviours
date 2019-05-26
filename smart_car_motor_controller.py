from dual_motor_controller import DualMotorController
from gpiozero import Motor

MAX_SPEED_M_PER_SEC = 0.52


class SmartCarMotorController(DualMotorController):
    def __init__(self):
        super(SmartCarMotorController, self).__init__()
        self._left_motor = Motor(4, 14)
        self._right_motor = Motor(18, 17)

    def set_speeds(self, speed_left_m_per_sec, speed_right_m_per_sec):
        print(str(speed_left_m_per_sec), str(speed_right_m_per_sec))
        speed_left = speed_left_m_per_sec / MAX_SPEED_M_PER_SEC
        speed_right = speed_right_m_per_sec / MAX_SPEED_M_PER_SEC

        if speed_left < 0:
            self._left_motor.backward(-speed_left)
        else:
            self._left_motor.forward(speed_left)

        if speed_right < 0:
            self._right_motor.backward(-speed_right)
        else:
            self._right_motor.forward(speed_right)
