from abc import abstractmethod


class DualMotorController:
    """
    Abstract base class for dual motor controllers.
    """
    @abstractmethod
    def set_speeds(self, speed_left, speed_right):
        """
        Set left and right motor speeds
        :param speed_left: in m/sec
        :param speed_right: in m/sec
        """
        pass
