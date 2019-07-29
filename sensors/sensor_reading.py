class SensorReading:
    """
    Class to hold sensor readings. Has a name of the sensor
    and the value of the sensor.
    """
    def __init__(self):
        self._name = None
        self._value = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
