""" dincase-mb3pico - Test the 3 outputs of connector to BackPlane board """

from machine import Pin
import time

out_pins = [Pin.board.GP16, Pin.board.GP17, Pin.board.GP18 ]

outputs = []
for pin in out_pins:
	outputs.append( Pin(pin,Pin.OUT) )

while True:
	for pin in outputs:
		pin.toggle()
		time.sleep_ms( 300 )
