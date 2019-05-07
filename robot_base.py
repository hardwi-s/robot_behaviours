class RobotBase:

    def __init__(self, wheel_separation, max_speed, motor_controller):
        self.__wheel_separation = wheel_separation
        self.__max_motor_speed = max_speed
        self.__motor_controller = motor_controller

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

    def do_motion_command(self, command):
        angular_speed = command.rotation * self.__wheel_separation

        speed_left = command.velocity - angular_speed
        speed_right = command.velocity + angular_speed

        # Adjust speeds if they exceed the maximum.
        if max(speed_left, speed_right) > self.__max_motor_speed:
            factor = self.__max_motor_speed / max(speed_left, speed_right)
            speed_left *= factor
            speed_right *= factor
        self.__motor_controller.set_speeds(speed_left, speed_right)
