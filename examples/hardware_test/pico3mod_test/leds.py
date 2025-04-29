""" dincase-mb3pico - Test the 4 LEDs and Status LED """

from machine import Pin, I2C
from pca9536 import PCA9536
import time

status = Pin( Pin.board.GP14, Pin.OUT)

i2c = I2C(1, sda=Pin.board.GP6, scl=Pin.board.GP7 )
leds = PCA9536( i2c )
for pin in range(4):
	leds.setup( pin, Pin.OUT )
for pin in range(4):
	leds.output( pin, False )


while True:
	for pin in range(4):
		status.toggle()
		leds.output( pin, True )
		time.sleep( 1 )
		leds.output( pin, False )
