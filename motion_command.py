class MotionCommand:
    """
    Holds a motion command. Motion is in the form
    of a velocity in m/sec and a rotation in rad/sec
    """
    def __init__(self, velocity=0.0, rotation=0.0):
        self._velocity = velocity
        self._rotation = rotation

    @property
    def velocity(self):
        return self._velocity

    @property
    def rotation(self):
        return self._rotation

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
