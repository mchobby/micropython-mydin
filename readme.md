# DinCase 3 modules MidBoard with Raspberry-Pi Pico 2 W
This repository contains the MicroPython code for MB3Pico controler board.

The MB3Pico is a controler board for 3 Modules DinCase designed to run with various backplane board (the High Power board located at the bottom of the DinCase).
The MB3Pico is properled with a Raspberry-Pi Pico 2 Wireless (RP2350 mcu) running under MicroPython.

The MB3Pico features:

* Power LED (Green)
* RunApp footprint (used to halt software)
* RTC Clock (DS3231, low drift)
* Piezzo Buzzer
* __User interface__
  * 4 outputs LEDs (Orange)
  * 4 inputs buttons
  * 1 status LED (red)
  * Reset button
* __Front panel Expansion connectors__
  * 1Wire bus with easy spring connector
  * I2C bus with Qwiic/StemmaQT interface (JST-SH4)
  * I2C, SPI, UART, Power with UEXT interface (IDC 2x5)
* Option Qwiic/StemmaQt footprint under the PCB for inner DinCase I2C expansion.
* 3V3 Interface with BackPlane
  * 3 outputs 
  * 2 inputs (one also being analog input)

Pico 2 Wireless features:

* 150 MHz Dual Core Cortex M33 with FPU
* 512 KB RAM
* 4 MB flash
* WiFi
* Bluetooth
* micro-USB (programming diagnostic)

# Available BackPlanes
## 2 relays modules
__Code Name:__ DINCASE-2R-BP3MOD

That board features a 2 opto-isolated relays capable of interrupting a current of 10 amps under 250V AC. Relays offer NO contacts.

# Examples

This product comes with many examples. They are detailled in the [examples/readme.md](examples/readme_ENG.md) file.

