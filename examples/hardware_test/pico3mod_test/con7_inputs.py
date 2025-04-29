""" dincase-mb3pico - Test the 2 inputs of connector to BackPlane board """

from machine import Pin
import time

in_pins = [Pin.board.GP27, Pin.board.GP19 ]

inputs = []
for pin in in_pins:
	inputs.append( Pin(pin,Pin.IN,Pin.PULL_UP) )

while True:
	print( ','.join( [str(_in.value()) for _in in inputs] ) )
	time.sleep_ms( 300 )
