class SensorReading:
    def __init__(self):
        self.__name = None
        self.__value = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value
