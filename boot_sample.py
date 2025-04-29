from machine import Pin

RUN_APP = Pin.board.GP3  # High=Run, Low=Stop

if Pin( RUN_APP, Pin.IN, Pin.PULL_UP ).value()==False:
	print( '[BOOT] skip execution (RUN_APP is false)' )
else:
	print( '[BOOT] entering...' )

	# >>> PLACE BOOT CODE HERE <<<


	print( '[BOOT] exit' )