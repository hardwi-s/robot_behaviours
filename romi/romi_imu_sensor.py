class RomiImuSensor:
    """
    Class for Romi inertial measurement unit.
    """
    def __init__(self, name, a_star):
        self._name = name
        self._a_star = a_star

    def get_value(self):
        return self._a_star.read_imu()

    def get_name(self):
        return self._name
