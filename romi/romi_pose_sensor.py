from threading import Lock


class RomiPoseSensor:
    def __init__(self, name='pose', pose=None, base=None):
        self._name = name
        if pose is None:
            pose = {'x': 0.0, 'y': 0.0, 'theta': 0.0}
        self._pose = pose
        self._base = base
        self._lock = Lock()

    def _update(self):
        current_motion_command = self._base.get_motion_command()
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
