
# The Arduino two-wire interface uses a 7-bit number for the address,
# and sets the last bit correctly based on reads and writes

from romi.lsm6_includes import *

DS33_SA0_HIGH_ADDRESS = 0b1101011
DS33_SA0_LOW_ADDRESS = 0b1101010
TEST_REG_ERROR = -1
DS33_WHO_ID = 0x69

class Lsm6:
    def __init__(self):
        self._device = device_auto
        self._address = None
        self._io_timeout = 0  # 0 = no timeout
        self._did_timeout = False
        self._a = [] # accelerometer readings
        self._g = [] # gyro readings
        self._last_status = None # status of last I2C transmission

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
        if device == device_auto || sa0 == sa0_auto:
            # check for LSM6DS33 if device is unidentified or was specified to be this type
            if device == device_auto || device == device_DS33:
                # check SA0 high address unless SA0 was specified to be low
                if sa0 != sa0_low and testReg(DS33_SA0_HIGH_ADDRESS, WHO_AM_I) == DS33_WHO_ID:
                    sa0 = sa0_high
                    if device == device_auto:
                        device = device_DS33
                # check SA0 low address unless SA0 was specified to be high
                elif sa0 != sa0_high and testReg(DS33_SA0_LOW_ADDRESS, WHO_AM_I) == DS33_WHO_ID:
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
void
LSM6::enableDefault(void)
{
if (_device == device_DS33)
    {
        # Accelerometer

        # 0x80 = 0b10000000
        # ODR = 1000 (1.66 kHz (high performance)); FS_XL = 00 (+/-2 g full scale)
        writeReg(CTRL1_XL, 0x80);

# Gyro

# 0x80 = 0b010000000
# ODR = 1000 (1.66 kHz (high performance)); FS_XL = 00 (245 dps)
writeReg(CTRL2_G, 0x80);

# Common

# 0x04 = 0b00000100
# IF_INC = 1 (automatically increment register address)
writeReg(CTRL3_C, 0x04);
}
}

void
LSM6::writeReg(uint8_t
reg, uint8_t
value)
{
Wire.beginTransmission(address);
Wire.write(reg);
Wire.write(value);
last_status = Wire.endTransmission();
}

uint8_t
LSM6::readReg(uint8_t
reg)
{
uint8_t
value;

Wire.beginTransmission(address);
Wire.write(reg);
last_status = Wire.endTransmission();
Wire.requestFrom(address, (uint8_t)
1);
value = Wire.read();
Wire.endTransmission();

return value;
}

# Reads the 3 accelerometer channels and stores them in vector a
void
LSM6::readAcc(void)
{
Wire.beginTransmission(address);
# automatic increment of register address is enabled by default (IF_INC in CTRL3_C)
Wire.write(OUTX_L_XL);
Wire.endTransmission();
Wire.requestFrom(address, (uint8_t)
6);

uint16_t
millis_start = millis();
while (Wire.available() < 6) {
if (io_timeout > 0 & & ((uint16_t)millis() - millis_start) > io_timeout)
{
did_timeout = true;
return;
}
}

uint8_t
xla = Wire.read();
uint8_t
xha = Wire.read();
uint8_t
yla = Wire.read();
uint8_t
yha = Wire.read();
uint8_t
zla = Wire.read();
uint8_t
zha = Wire.read();

# combine high and low bytes
a.x = (int16_t)(xha << 8 | xla);
a.y = (int16_t)(yha << 8 | yla);
a.z = (int16_t)(zha << 8 | zla);
}

# Reads the 3 gyro channels and stores them in vector g
void
LSM6::readGyro(void)
{
    Wire.beginTransmission(address);
# automatic increment of register address is enabled by default (IF_INC in CTRL3_C)
Wire.write(OUTX_L_G);
Wire.endTransmission();
Wire.requestFrom(address, (uint8_t)
6);

uint16_t
millis_start = millis();
while (Wire.available() < 6) {
if (io_timeout > 0 & & ((uint16_t)millis() - millis_start) > io_timeout)
{
did_timeout = true;
return;
}
}

uint8_t
xlg = Wire.read();
uint8_t
xhg = Wire.read();
uint8_t
ylg = Wire.read();
uint8_t
yhg = Wire.read();
uint8_t
zlg = Wire.read();
uint8_t
zhg = Wire.read();

# combine high and low bytes
g.x = (int16_t)(xhg << 8 | xlg);
g.y = (int16_t)(yhg << 8 | ylg);
g.z = (int16_t)(zhg << 8 | zlg);
}

# Reads all 6 channels of the LSM6 and stores them in the object variables
void
LSM6::read(void)
{
    readAcc();
readGyro();
}

void
LSM6::vector_normalize(vector < float > * a)
{
    float
mag = sqrt(vector_dot(a, a));
a->x /= mag;
a->y /= mag;
a->z /= mag;
}

# Private Methods //////////////////////////////////////////////////////////////

int16_t
LSM6::testReg(uint8_t
address, regAddr
reg)
{
    Wire.beginTransmission(address);
Wire.write((uint8_t)
reg);
if (Wire.endTransmission() != 0)
{
return TEST_REG_ERROR;
}

Wire.requestFrom(address, (uint8_t)
1);
if (Wire.available())
{
return Wire.read();
}
else
{
return TEST_REG_ERROR;
}
}
