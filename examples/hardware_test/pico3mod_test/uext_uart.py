""" dincase-mb3pico - Test the UEXT UART """
from machine import Pin, UART
import time

# UART(1)
UART_RX = Pin.board.GP5
UART_TX = Pin.board.GP4

# See MicroPython UART documentation 
# https://docs.micropython.org/en/latest/library/machine.UART.html
#
uart = UART( 1, rx=UART_RX, tx=UART_TX, baudrate=115200 )
uart.write( "Small message".encode('ASCII') )
