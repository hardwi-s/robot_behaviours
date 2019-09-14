import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from time import sleep
from sensors.lsm6ds33 import LSM6DS33


class RomiImuSensor:
    """
    Class for Romi inertial measurement unit.
    """
    def __init__(self, name):
        self._name = name
        self._imu = LSM6DS33()
        self._imu.enableLSM()

    def get_value(self):
        return self._imu.getAllRaw()

    def get_name(self):
        return self._name


if __name__ == '__main__':
    imu = RomiImuSensor(name='imu')
    while True:
        values = imu.get_value()
        print('accel ' + str(values[0]) + ' ' + str(values[1]) + ' ' + str(values[2])
              + ' gyro  ' + str(values[3]) + ' ' + str(values[4]) + ' ' + str(values[5]))
        sleep(.25)
