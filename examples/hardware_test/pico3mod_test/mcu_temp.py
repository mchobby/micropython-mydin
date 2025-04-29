# Based on Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-internal-temperature-micropython/

from machine import ADC

# Internal temperature sensor is connected to ADC channel 4
mcu_adc4 = ADC(4)

def mcu_temp():
	val = 0
	for i in range(10):
		val += mcu_adc4.read_u16()
	# Convert ADC value to voltage
	volt = (val/10) * (3.3 / 65535.0)
	# Temperature calculation based on sensor characteristics
	return 27 - (volt - 0.706) / 0.001721



t = mcu_temp()
print("Internal Temperature:", t, "°C")
