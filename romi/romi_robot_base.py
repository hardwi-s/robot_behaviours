from math import pi

from robot_base import RobotBase

TICKS_PER_REV = 1440.0
WHEEL_DIAMETER = 0.07
WHEEL_CIRCUMFERENCE = pi * WHEEL_DIAMETER
ROMI_ENCODER_INTERVAL = 50.0 / 1000.0   # 50 msec
TICKS_PER_M = TICKS_PER_REV / WHEEL_CIRCUMFERENCE


class RomiRobotBase(RobotBase):
    def __init__(self, wheel_separation, max_speed, sensors, a_star):
        super().__init__(wheel_separation, max_speed, sensors)
        self._a_star = a_star
        self._romi_speed_left = 0
        self._romi_speed_right = 0

    def do_motion_command(self, command):
        """
        Convert motion to left and right motor speeds and sets
        these in the controller
        :param command: The motion as a MotionCommand
        """
        if command:
            angular_speed = command.rotation * self._wheel_separation

            speed_left = command.velocity - angular_speed
            speed_right = command.velocity + angular_speed

            # Adjust speeds if they exceed the maximum.
            if max(speed_left, speed_right) > self._max_motor_speed:
                factor = self._max_motor_speed / max(speed_left, speed_right)
                speed_left *= factor
                speed_right *= factor

            # Speeds are in m/sec, convert to Romi speeds
            romi_speed_left = self._romi_speed(speed_left)
            romi_speed_right = self._romi_speed(speed_right)
            if (romi_speed_left != self._romi_speed_left) or (romi_speed_right != self._romi_speed_right):
                self._romi_speed_left = romi_speed_left
                self._romi_speed_right = romi_speed_right
                self._a_star.motors(self._romi_speed_left, self._romi_speed_right)

    def _romi_speed(self, motor_speed_m_per_sec):
        '''
        1 m/sec = (1440 / (pi * 0.07)) * 0.05 ticks/cycle
        speed = m/sec * 327.42
        :param motor_speed_m_per_sec:
        :return: motor speed in ticks per loop
        '''
        return int((motor_speed_m_per_sec * TICKS_PER_M) * ROMI_ENCODER_INTERVAL)
