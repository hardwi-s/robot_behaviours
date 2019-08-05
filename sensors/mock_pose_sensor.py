from math import atan


class MockPoseSensor:
    def __init__(self, name='mock_pose'):
        self._name = name
        self._x = 0.0
        self._y = 0.0
        self._theta = 0.0
        self._value = {'x': 0.0, 'y': 0.0, 'theta': 0.0}

    @property
    def value(self):
        self._x = self._x + 1
        self._y = self._y + 1
        self._theta = atan(1)
        return {'x': self._x, 'y': self._y, 'theta': self._theta}

    @property
    def name(self):
        return self._name

    def reset(self):
        self._x = 0.0
        self._y = 0.0
        self._theta = 0.0
