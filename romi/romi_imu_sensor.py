class RomiImuSensor:
    """
    Class for Romi inertial measurement unit.
    """
    def __init__(self, name):
        self._name = name

    def get_value(self):
        return None

    def get_name(self):
        return self._name
