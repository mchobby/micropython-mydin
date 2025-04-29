""" dincase-mb3pico - Test the UEXT UART """
from machine import Pin, SPI
import time

# SPI(1)
SPI_MOSI = Pin.board.GP11
SPI_MISO = Pin.board.GP8
SPI_SCK  = Pin.board.GP10
SPI_SSEL = Pin.board.GP9

# See MicroPython SPI documentation 
# https://docs.micropython.org/en/latest/library/machine.SPI.html
#
sel = Pin( SPI_SSEL, Pin.OUT, value=True ) # SPI transaction starts witb LOW
spi = SPI( 1, mosi=SPI_MOSI, miso=SPI_MISO, sck=SPI_SCK, baudrate=2_000_000 )

sel.value( 0 ) # Start transaction 
spi.write( "SOMEDATA".encode('ASCII') )
sel.value( 1 ) # End transaction 
