from robot_base import RobotBase

TICKS_PER_REV = 1440.0
WHEEL_DIAMETER = 0.07


class RomiRobotBase(RobotBase):
    def __init__(self, wheel_separation, max_speed, sensors, a_star):
        super().__init__(wheel_separation, max_speed, sensors)
        self._a_star = a_star

    def do_motion_command(self, command):
        """
        Convert motion to left and right motor speeds and sets
        these in the controller
        :param command: The motion as a MotionCommand
        """
        angular_speed = command.rotation * self._wheel_separation

        speed_left = command.velocity - angular_speed
        speed_right = command.velocity + angular_speed

        # Adjust speeds if they exceed the maximum.
        if max(speed_left, speed_right) > self._max_motor_speed:
            factor = self._max_motor_speed / max(speed_left, speed_right)
            speed_left *= factor
            speed_right *= factor

        # Speeds are in m/sec, convert to Romi speeds
        self._a_star.motors(self._romi_speed(speed_left), self._romi_speed(speed_right))

    def _romi_speed(self, motor_speed):
        return motor_speed
