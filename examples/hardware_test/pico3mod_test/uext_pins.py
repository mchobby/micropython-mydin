""" dincase-mb3pico - Test the UEXT UART """
from machine import Pin
import time

# == UEXT UART Pins =====================
UART_RX = Pin.board.GP5
UART_TX = Pin.board.GP4

# Uart pins can be driven as INPUT or OUTPUT instead as an UART
rx_pin = Pin( UART_RX, Pin.OUT )
tx_pin = Pin( UART_TX, Pin.OUT )

rx_pin.on() # or off() or value()
tx_pin.off()

# == UEXT SPI Pins =====================
SPI_MOSI = Pin.board.GP11
SPI_MISO = Pin.board.GP8
SPI_SCK  = Pin.board.GP10
SPI_SSEL = Pin.board.GP9

# Uart pins can be driven as INPUT or OUTPUT instead as a SPI bus
mosi_pin = Pin( SPI_MOSI, Pin.OUT )
miso_pin = Pin( SPI_MISO, Pin.OUT )
sck_pin  = Pin( SPI_SCK,  Pin.OUT )
ssel_pin = Pin( SPI_SSEL, Pin.OUT )

mosi_pin.off()
miso_pin.off()
sck_pin.off()
ssel_pin.on()

# == UEXT I2C Pins =====================

# UEXT I2C bus is also wired to internal 
# I2C clock. Its pins cannot be reused for 
# other purpose
# 
