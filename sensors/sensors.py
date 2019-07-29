from sensors.sensor_reading import SensorReading


class Sensors:
    def __init__(self, sensors=None):
        if sensors is None:
            sensors = []
        self._sensors = sensors

    def read_sensors(self):
        """
        Reads all the robot sensors
        :return: A list of SensorReading
        """
        return_values = []
        for sensor in self._sensors:
            reading = SensorReading()
            reading.name = sensor.name
            reading.value = sensor.value
            return_values.append(reading)
        return return_values
