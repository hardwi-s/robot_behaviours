from robot_base import RobotBase


class SmartCarRobotBase(RobotBase):
    def __init__(self, wheel_separation, max_speed, motor_controller, sensors):
        super().__init__(wheel_separation, max_speed, sensors)
        self._motor_controller = motor_controller

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
        self._motor_controller.set_speeds(speed_left, speed_right)
