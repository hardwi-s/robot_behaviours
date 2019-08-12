import time
import numpy as np

from romi.lsm6_includes import *

# The Arduino two-wire interface uses a 7-bit number for the address,
# and sets the last bit correctly based on reads and writes
DS33_SA0_HIGH_ADDRESS = 0b1101011
DS33_SA0_LOW_ADDRESS = 0b1101010
TEST_REG_ERROR = -1
DS33_WHO_ID = 0x69


def millis():
    return int(round(time.time() * 1000))


def vector_normalize(a):
    return np.linalg.norm(a)


def test_reg(address, reg):
    Wire.beginTransmission(address)
    Wire.write(reg)
    if Wire.endTransmission() != 0:
        return TEST_REG_ERROR

    Wire.requestFrom(address, 1)
    if Wire.available():
        return Wire.read()
    else:
        return TEST_REG_ERROR


class Lsm6:
    def __init__(self):
        self._device = device_auto
        self._address = None
        self._io_timeout = 0  # 0 = no timeout
        self._did_timeout = False
        self._a = np.array([0, 0, 0])  # accelerometer readings
        self._g = np.array([0, 0, 0])  # gyro readings
        self._last_status = None  # status of last I2C transmission

    # Did a timeout occur in readAcc(), readGyro(), or read() since the last call to timeoutOccurred()?
    def timeout_occurred(self):
        tmp = self._did_timeout
        self._did_timeout = False
        return tmp

    def set_timeout(self, timeout):
        self._io_timeout = timeout

    def get_timeout(self):
        return self._io_timeout

    def init(self, device, sa0):
        # perform auto-detection unless device type and SA0 state were both specified
        if device == device_auto or sa0 == sa0_auto:
            # check for LSM6DS33 if device is unidentified or was specified to be this type
            if device == device_auto or device == device_DS33:
                # check SA0 high address unless SA0 was specified to be low
                if sa0 != sa0_low and test_reg(DS33_SA0_HIGH_ADDRESS, WHO_AM_I) == DS33_WHO_ID:
                    sa0 = sa0_high
                    if device == device_auto:
                        device = device_DS33
                # check SA0 low address unless SA0 was specified to be high
                elif sa0 != sa0_high and test_reg(DS33_SA0_LOW_ADDRESS, WHO_AM_I) == DS33_WHO_ID:
                    sa0 = sa0_low
                    if device == device_auto:
                        device = device_DS33
            # make sure device and SA0 were successfully detected; otherwise, indicate failure
            if device == device_auto or sa0 == sa0_auto:
                return False

        self._device = device

        if device == device_DS33:
            if sa0 == sa0_high:
                self._address = DS33_SA0_HIGH_ADDRESS
            else:
                self._address = DS33_SA0_LOW_ADDRESS

        return True

    '''
    Enables the LSM6 's accelerometer and gyro. Also:
    - Sets sensor full scales(gain) to default power - on values, which are + / - 2g for accelerometer and 245 dps for gyro
    - Selects 1.66 kHz (high performance) ODR (output data rate) for accelerometer and 1.66 kHz (high performance) ODR for gyro.
    (These are the ODR settings for which the electrical characteristics are specified in the datasheet.)
    - Enables automatic increment of register address during multiple byte access Note that this function will
    also reset other settings controlled by the registers it writes to.
    '''
    def enable_default(self):
        if self._device == device_DS33:
            # Accelerometer

            # 0x80 = 0b10000000
            # ODR = 1000 (1.66 kHz (high performance)); FS_XL = 00 (+/-2 g full scale)
            self.write_reg(CTRL1_XL, 0x80)

            # Gyro

            # 0x80 = 0b010000000
            # ODR = 1000 (1.66 kHz (high performance)); FS_XL = 00 (245 dps)
            self.write_reg(CTRL2_G, 0x80)

            # Common

            # 0x04 = 0b00000100
            # IF_INC = 1 (automatically increment register address)
            self.write_reg(CTRL3_C, 0x04)

    def write_reg(self, reg, reg_value):
        Wire.beginTransmission(self._address)
        Wire.write(reg)
        Wire.write(reg_value)
        self._last_status = Wire.endTransmission()

    def read_reg(self, reg):
        Wire.beginTransmission(self._address)
        Wire.write(reg)
        self._last_status = Wire.endTransmission()
        Wire.requestFrom(self._address, 1)
        value = Wire.read()
        Wire.endTransmission()
        return value

    # Reads the 3 accelerometer channels and stores them in vector a
    def read_acc(self):
        Wire.beginTransmission(self._address)
        # automatic increment of register address is enabled by default (IF_INC in CTRL3_C)
        Wire.write(OUTX_L_XL)
        Wire.endTransmission()
        Wire.requestFrom(self._address, 6)

        millis_at_start = millis()
        while Wire.available() < 6:
            if 0 < self._io_timeout < (millis() - millis_at_start):
                self._did_timeout = True
                return

        xla = Wire.read()
        xha = Wire.read()
        yla = Wire.read()
        yha = Wire.read()
        zla = Wire.read()
        zha = Wire.read()

        # combine high and low bytes
        self._a[0] = (xha << 8 | xla)
        self._a[1] = (yha << 8 | yla)
        self._a[2] = (zha << 8 | zla)

    # Reads the 3 gyro channels and stores them in vector g
    def read_gyro(self):
        Wire.beginTransmission(self._address)
        # automatic increment of register address is enabled by default (IF_INC in CTRL3_C)
        Wire.write(OUTX_L_G)
        Wire.endTransmission()
        Wire.requestFrom(self._address, 6)

        millis_at_start = millis()
        while Wire.available() < 6:
            if 0 < self._io_timeout < (millis() - millis_at_start):
                self._did_timeout = True
                return;

        xlg = Wire.read()
        xhg = Wire.read()
        ylg = Wire.read()
        yhg = Wire.read()
        zlg = Wire.read()
        zhg = Wire.read()

        # combine high and low bytes
        self._g[0] = (xhg << 8 | xlg)
        self._g[1] = (yhg << 8 | ylg)
        self._g[2] = (zhg << 8 | zlg)

    # Reads all 6 channels of the LSM6 and stores them in the object variables
    def read(self):
        self.read_acc()
        self.read_gyro()

    def get_acc(self):
        return self._a

    def get_gyro(self):
        return self._g
