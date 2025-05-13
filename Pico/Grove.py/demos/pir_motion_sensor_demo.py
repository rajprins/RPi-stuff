from machine import Pin,ADC,PWM
from time import sleep
import utime

miniPir = Pin(18, Pin.IN)

i=0
j=0
while True:
    if miniPir.value() == 1 :
        i+=1
        print('[',i,'] Motion detected!')
        sleep(1)
    else:
        j+=1
        print('[',j,'] All quiet.')
        sleep(1)