""" dincase-mb3pico - Test the UEXT UART """
from machine import Pin, I2C
import time

# I2C(1)
I2C_SDA = Pin.board.GP6
I2C_SCL = Pin.board.GP7

# See MicroPython I2C documentation 
# https://docs.micropython.org/en/latest/library/machine.I2C.html
#
i2c = I2C( 1, sda=I2C_SDA, scl=I2C_SCL, freq=400000 )
print( i2c.scan() )

# IMPORTANT REMARKs ---------------------------------
#
#   The DinControler already expose the I2C bus.
#   No need to create a new instance for it.
#
#   See examples/din_controler/async_qwiic_serlcd.py
#
# ----------------------------------------------------
