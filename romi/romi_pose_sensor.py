from math import cos, sin, pi
from threading import Lock

from motion_command import MotionCommand
from robot_base import RobotBase


class RomiPoseSensor:
    def __init__(self, name='pose', pose=None, base=None, encoders=None):
        self._name = name
        if pose is None:
            print('Using default initial pose')
            pose = {'x': 0.0, 'y': 0.0, 'theta': 0.0}
        self._pose = pose
        self._base = base
        self._encoders = encoders
        self._old_left_encoder = 0
        self._old_right_encoder = 0

    def _update(self):
        current_motion_command = self._base.get_motion_command()
        new_encoder_values = self._encoders.get_value()
        if current_motion_command is not None:
            if current_motion_command.rotation == 0.0:
                # Calculate the distance travelled
                left_distance = new_encoder_values[0] - self._old_left_encoder
                right_distance = new_encoder_values[1] - self._old_right_encoder
                new_distance = (left_distance + right_distance) / 2
                # Resolve into components
                new_x_component = new_distance * cos(self._pose['theta'])
                new_y_component = new_distance * sin(self._pose['theta'])
                # Update pose
                self._pose['x'] = self._pose['x'] + new_x_component
                self._pose['y'] = self._pose['y'] + new_y_component
            elif current_motion_command.velocity == 0.0:
                left_distance = -(new_encoder_values[0] - self._old_left_encoder)
                right_distance = new_encoder_values[1] - self._old_right_encoder
                # Calculate the new angle and update pose
                angle = (left_distance + right_distance)/self._base.get_wheel_separation()
                self._pose['theta'] = (self._pose['theta'] + angle) % (2 * pi)
            else:
                print('Invalid motion command for pose estimation')
                pass
        # Save new encoder values
        self._old_left_encoder = new_encoder_values[0]
        self._old_right_encoder = new_encoder_values[1]

    def get_value(self):
        self._update()
        return self._pose

    def get_name(self):
        return self._name


if __name__ == '__main__':

    class MockBase(RobotBase):
        def __init__(self, wheel_separation, max_speed):
            super().__init__(wheel_separation, max_speed)
            self._motion_command = MotionCommand()

        def get_motion_command(self):
            return self._motion_command

        def set_motion_command(self, command):
            self._motion_command = command


    class MockEncoders:
        def __init__(self, base):
            self._dist_left = 0.0
            self._dist_right = 0.0
            self._base = base
            self._count = 0

        def get_value(self):
            motion = self._base.get_motion_command()
            self._count = self._count + 1
            if motion.rotation == 0.0:
                self._dist_left = self._dist_left + motion.velocity
                self._dist_right = self._dist_left
            elif motion.velocity == 0.0:
                self._dist_left = self._dist_left - motion.rotation
                self._dist_right = self._dist_right + motion.rotation
            return [self._dist_left, self._dist_right]


    wheel_separation = 0.133  # metres
    max_speed = 0.61
    mock_base = MockBase(wheel_separation, max_speed)
    mock_base.set_motion_command(MotionCommand(velocity=1.0, rotation=0.0))
    pose_sensor = RomiPoseSensor(name='pose', pose={'x': 0.0, 'y': 0.0, 'theta': 0.0},
                                 base=mock_base, encoders=MockEncoders(base=mock_base))
    for i in range(0, 10):
        print(pose_sensor.get_value)
    mock_base.set_motion_command(MotionCommand(velocity=0.0, rotation=0.01))
    for i in range(0, 10):
        print(pose_sensor.get_value)
