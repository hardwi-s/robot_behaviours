from abc import ABCMeta, abstractmethod
from sensor_reading import SensorReading


class RobotBase(metaclass=ABCMeta):
    def __init__(self, wheel_separation, max_speed, sensors):
        """

        :param wheel_separation: in metres
        :param max_speed: in m/sec
        """
        self._wheel_separation = wheel_separation
        self._max_motor_speed = max_speed
        self._sensors = sensors

    def get_wheel_separation(self):
        return self._wheel_separation

    def set_wheel_separation(self, separation):
        self._wheel_separation = separation

    def get_max_motor_speed(self):
        return self._max_motor_speed

    def set_max_motor_speed(self, limit):
        self._max_motor_speed = limit

    @abstractmethod
    def do_motion_command(self, command):
        """
        Convert motion to left and right motor speeds and sets
        these in the controller
        :param command: The motion as a MotionCommand
        """
        pass

    def read_sensors(self):
        """
        Reads all the base sensors
        :return: A list of SensorReading
        """
        return_values = []
        for sensor in self._sensors:
            reading = SensorReading()
            reading.name = sensor.name
            reading.value = sensor.value
            return_values.append(reading)
        return return_values
