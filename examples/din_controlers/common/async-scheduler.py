# Run scheduled JOBs while running the DIN Controler Tasks
#
#   The scheduler executes jobs at the best scheduling possible
#     and ONLY ONE JOB is run at a time.
#
#   Do not confuse with asyncio tasks that are running concurrently
#     - one task for the loop()
#     - one task for the scheluder.run_forever()
# 
# Hardware Configuration; DINCASE-2R-BP3MOD (2 relays backplane) + DINCASE-PICO-3MOD (Pico 2 Wireless MidBoard) 
# 
# See project: http://github/mchobby/micropython-mydin
#
from mydin import configure
from mydin.pico import Pico3Mod
from mydin.backplane.relays import TwoRelay3Mod 
import time, sys, asyncio

import schedule

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )

# === Define & schedule Jobs ==================
async def job_relay2():
	global din
	din.rel2.on()
	din.leds[1].on()
	await asyncio.sleep(30) # Wait 30 Sec
	din.leds[1].off()


async def job_toggle_led( led_idx ): # Job with parameter
	global din
	din.leds[led_idx].toggle()

schedule.every(1).minutes.do( job_relay2 )
schedule.every(3).seconds.do( job_toggle_led, 2 ) # Toggle led 2 of 0..3
schedule.every(7).seconds.do( job_toggle_led, 3 ) # Toggle led 3 of 0..3
# --- Other exemples of scheduling ---
# schedule.every(10).seconds.do(job_with_argument, name="MicroPython")
# for h in range( 8, 17 ):
# 	schedule.every().day.at("%02i:00" % h).do( upd_auth_file_job, drawer )
# schedule.every().day.at("20:00").do( upl_log_file_job, drawer )

# === Main DIN tasks ===================
counter = 0
async def loop( din ):
	""" called again and again (like Arduino) """
	global counter
	counter += 1
	# Place your loop code here
	print( "loop iteration %3i " % (counter ) )
	await asyncio.sleep( 5 )


# === Running Din Project ==============
def create_tasks( async_evloop ): # called by din.setup() 
	# new task to register the scheduler runtime
	scheduler_task = async_evloop.create_task( schedule.run_forever() )

din.setup( setup=None, loop=loop, on_tasks_create=create_tasks )
din.run()