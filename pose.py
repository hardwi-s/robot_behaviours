class Pose:
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self._x = x
        self._y = y
        self._theta = theta

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def theta(self):
        return self._theta

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @theta.setter
    def theta(self, value):
        self._theta = value
