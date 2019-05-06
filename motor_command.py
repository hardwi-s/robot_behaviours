class MotorCommand:

    def __init__(self):
        self.__left_speed = 0.0
        self.__right_speed = 0.0

    @property
    def left_speed(self):
        return self.__left_speed

    @property
    def right_speed(self):
        return self.__right_speed

    @left_speed.setter
    def left_speed(self, value):
        self.__left_speed = value

    @right_speed.setter
    def right_speed(self, value):
        self.__right_speed = value
