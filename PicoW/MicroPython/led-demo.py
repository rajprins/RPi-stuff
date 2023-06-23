from machine import Pin
import time

led = Pin("LED", Pin.OUT)

while True:       # Herhaal tot het programma gestopt wordt
    led.on()      # Schakel de LED in
    time.sleep(1) # Wacht 1 seconde
    led.off()     # Schakel de LED uit
    time.sleep(1) # Wacht 1 seconde