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
        return self._imu.getAllScaled()

    def get_name(self):
        return self._name


if __name__ == '__main__':
    imu = RomiImuSensor(name='imu')
    while True:
        values = imu.get_value()
        print('accel {0:7.3f} {1:7.3f} {2:7.3f} gyro {3:7.3f} {4:7.3f} {5:7.3f} temp {6:7.1f}'
              .format(values[0], values[1], values[2], values[3], values[4], values[5], values[6]))
        sleep(.25)
