from threading import Lock


class RomiPoseSensor:
    def __init__(self, name='pose', pose=None, base=None, encoders=None):
        self._name = name
        if pose is None:
            pose = {'x': 0.0, 'y': 0.0, 'theta': 0.0}
        self._pose = pose
        self._base = base
        self._encoders = encoders
        self._lock = Lock()

    def _update(self):
        current_motion_command = self._base.get_motion_command()
        new_encoders = self._encoders.value
        distance_left = new_encoders[0]
        distance_right = new_encoders[1]
        with self._lock:
            if current_motion_command.rotation == 0:
                pass
            elif current_motion_command.velocity == 0:
                pass
            else:
                pass

    @property
    def value(self):
        with self._lock:
            self._update()
            return self._pose

    @property
    def name(self):
        return self._name
