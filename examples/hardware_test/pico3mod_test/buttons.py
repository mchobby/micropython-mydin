""" dincase-mb3pico - Test the 4 buttons input """
from machine import Pin
import time

btn_pins = [Pin.board.GP20,Pin.board.GP21,Pin.board.GP22,Pin.board.GP26]

btns = []
for pin in btn_pins:
	btns.append( Pin(pin, Pin.IN, Pin.PULL_UP) )

while True:
	print( ",".join([str(btn.value()) for btn in btns]) )
	time.sleep_ms( 300 )