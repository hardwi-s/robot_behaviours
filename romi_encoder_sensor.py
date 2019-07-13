class RomiEncoderSensor:
    """
    Class for Romi position encoder measurement.
    """
    def __init__(self, name, a_star):
        self._name = name
        self._a_star = a_star

    @property
    def value(self):
        return self._a_star.read_encoders_total()

    @property
    def name(self):
        return self._name
