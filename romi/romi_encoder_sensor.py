class RomiEncoderSensor:
    """
    Class for Romi position encoder measurement.
    """
    def __init__(self, name, a_star):
        self._name = name
        self._a_star = a_star

    def get_value(self):
        return self._a_star.read_encoders_total()

    def get_name(self):
        return self._name
