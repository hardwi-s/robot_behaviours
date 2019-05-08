class MotionCommand:
    """
    Holds a motion command. Motion is in the form
    of a velocity in m/sec and a rotation in rad/sec
    """
    def __init__(self, velocity=0.0, rotation=0.0):
        self.__velocity = velocity
        self.__rotation = rotation

    @property
    def velocity(self):
        return self.__velocity

    @property
    def rotation(self):
        return self.__rotation

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value

    @rotation.setter
    def rotation(self, value):
        self.__rotation = value
