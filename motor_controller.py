from abc import abstractmethod


class MotorController:

    @abstractmethod
    def set_speeds(self, speed_left, speed_right):
        pass
