#!/usr/bin/python

# Python module to control several aspects of Pololu's AltIMU-10v5 ###
#
# This file contains several constants used by the various module
# classes.
#
# The Python code is developed and maintained by
# Torsten Kurbad <github@tk-webart.de>
#
########################################################################

# Global constants

# I2C device addresses
LIS3MDL_ADDR = 0x1e  # Magnetometer
LPS25H_ADDR = 0x5d  # Barometric pressure sensor
LSM6DS33_ADDR = 0x6b  # Gyrometer / accelerometer

# Accelerometer gain in milli g per bit for different full scale values
ACCEL_GAIN_MG_2 = 0.061
ACCEL_GAIN_MG_4 = 0.122
ACCEL_GAIN_MG_8 = 0.244
ACCEL_GAIN_MG_16 = 0.488

# Gyro gain in milli deg/sec per bit for different full scale values
GYRO_GAIN_MDPS_125 = 4.375
GYRO_GAIN_MDPS_250 = 8.75
GYRO_GAIN_MDPS_500 = 17.50
GYRO_GAIN_MDPS_1000 = 35.0
GYRO_GAIN_MDPS_2000 = 70.0
