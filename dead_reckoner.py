from threading import Lock

from pose import Pose


class DeadReckoner:
    def __init__(self, pose=Pose()):
        self._pose = pose
        self._lock = Lock()

    def update(self, encoders, current_motion_command):
        with self._lock:
            if current_motion_command.rotation == 0:
                pass
            elif current_motion_command.velocity == 0:
                pass
            else:
                pass

    def get_pose(self):
        with self._lock:
            return self._pose
