""" dincase-mb3pico - check the RUN_APP status """

from machine import Pin, Signal
import time

run_app = Pin(Pin.board.GP3, Pin.IN, Pin.PULL_UP)

while True:
	print( 'RUN_APP=%s' % ('True' if run_app.value() else 'False') )
	time.sleep_ms(500)
