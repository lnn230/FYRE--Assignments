# Bliking Program

#incorpoorate mudules 
import machine #modelue with stuff from board 
import time #module with time stuff


#make led objects 
#green led is GPIO Pin 0
led = machine.Pin(0,machine.Pin.OUT)
#infinite loop
while True:
  led.value(1) #turns led on
  time.sleep(0.5) #0.5 second delay 
  led.value(0) #turn led off
  time.sleep(0.5) #delay again
