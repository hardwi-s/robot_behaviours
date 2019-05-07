class RobotBase:

    def __init__(self, wheel_separation, max_speed, ticks_per_metre):
        self.__wheel_separation = wheel_separation
        self.__max_motor_speed = max_speed
        self.__ticks_per_metre = ticks_per_metre

    @property
    def wheel_separation(self):
        return self.__wheel_separation

    @wheel_separation.setter
    def wheel_separation(self, separation):
        self.__wheel_separation = separation

    @property
    def max_motor_speed(self):
        return self.__max_motor_speed

    @max_motor_speed.setter
    def max_motor_speed(self, limit):
        self.__max_motor_speed = limit

    @property
    def ticks_per_metre(self):
        return self.__ticks_per_metre

    @ticks_per_metre.setter
    def ticks_per_metre(self, ticks):
        self.__ticks_per_metre = ticks
