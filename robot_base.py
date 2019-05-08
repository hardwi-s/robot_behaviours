from sensor_reading import SensorReading


class RobotBase:

    def __init__(self, wheel_separation, max_speed, motor_controller, sensors):
        """

        :param wheel_separation: in metres
        :param max_speed: in m/sec
        :param motor_controller: controller for wheel motors
        :param sensors: list of robot base sensors
        """
        self.__wheel_separation = wheel_separation
        self.__max_motor_speed = max_speed
        self.__motor_controller = motor_controller
        self.__sensors = sensors

    @property
    def wheel_separation(self):
        return self.__wheel_separation

    @wheel_separation.setter
    def wheel_separation(self, separation):
        self.__wheel_separation = separation

    @property
    def max_motor_speed(self):
        return self.__max_motor_speed

    @max_motor_speed.setter
    def max_motor_speed(self, limit):
        self.__max_motor_speed = limit

    def do_motion_command(self, command):
        """
        Convert motion to left and right motor speeds and sets
        these in the controller
        :param command: The motion as a MotionCommand
        """
        angular_speed = command.rotation * self.__wheel_separation

        speed_left = command.velocity - angular_speed
        speed_right = command.velocity + angular_speed

        # Adjust speeds if they exceed the maximum.
        if max(speed_left, speed_right) > self.__max_motor_speed:
            factor = self.__max_motor_speed / max(speed_left, speed_right)
            speed_left *= factor
            speed_right *= factor
        self.__motor_controller.set_speeds(speed_left, speed_right)

    def read_sensors(self):
        """
        Reads all the base sensors
        :return: A list of SensorReading
        """
        return_values = []
        for sensor in self.__sensors:
            reading = SensorReading()
            reading.name = sensor.name
            reading.value = sensor.value
            return_values.append(reading)
        return return_values