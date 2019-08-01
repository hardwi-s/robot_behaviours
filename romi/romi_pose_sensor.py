from math import cos, sin
from threading import Lock

from motion_command import MotionCommand


class RomiPoseSensor:
    def __init__(self, name='pose', pose=None, base=None, encoders=None):
        self._name = name
        if pose is None:
            pose = {'x': 0.0, 'y': 0.0, 'theta': 0.0}
        self._pose = pose
        self._base = base
        self._encoders = encoders
        self._old_left_encoder = 0
        self._old_right_encoder = 0
        self._lock = Lock()

    def _update(self):
        current_motion_command = self._base.get_motion_command()
        new_encoder_values = self._encoders.value
        if current_motion_command.rotation == 0:
            # Calculate the distance travelled
            left_distance = new_encoder_values[0] - self._old_left_encoder
            right_distance = new_encoder_values[1] - self._old_right_encoder
            new_distance = (left_distance + right_distance) / 2
            # Resolve into components
            new_x_component = new_distance * cos(self._pose['theta'])
            new_y_component = new_distance * sin(self._pose['theta'])
            # Update pose
            with self._lock:
                self._pose['x'] = self._pose['x'] + new_x_component
                self._pose['y'] = self._pose['y'] + new_y_component
        elif current_motion_command.velocity == 0:
            # Calculate the new angle
            # Update pose
            pass
        else:
            pass
        # Save new encoder values
        self._old_left_encoder = new_encoder_values[0]
        self._old_right_encoder = new_encoder_values[1]

    @property
    def value(self):
        self._update()
        with self._lock:
            return self._pose

    @property
    def name(self):
        return self._name


if __name__ == '__main__':

    class MockBase:
        def __init__(self):
            pass

        @staticmethod
        def get_motion_command():
            return MotionCommand(velocity=1.0, rotation=0.0)


    class MockEncoders:
        def __init__(self):
            self._count = 0
            self._dist = 0

        @property
        def value(self):
            self._count = self._count + 1
            if self._count < 5:
                self._dist = self._dist + 0.1
            else:
                self._dist = self._dist - 0.1
            return [self._dist, self._dist]


    pose_sensor = RomiPoseSensor(name='pose', pose={'x': 0.0, 'y': 0.0, 'theta': 1.0},
                                 base=MockBase(), encoders=MockEncoders())
    for i in range(0, 10):
        print(pose_sensor.value)
