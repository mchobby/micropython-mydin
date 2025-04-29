""" dincase-mb3pico - Testing I2C Qwiic connector  with BMP280 barometric sensor """

from machine import Pin, I2C
from bme280 import *
import time

i2c = I2C(1, sda=Pin.board.GP6, scl=Pin.board.GP7 )
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )

print( bmp.raw_values )

