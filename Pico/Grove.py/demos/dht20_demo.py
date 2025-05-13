##############################################################################
#
# MicroPython code for DHT20 temperature & humidity sensor
#
##############################################################################

from machine import I2C
from dht20 import DHT20
import utime


def setup():
    global dht20, i2c
    i2c = I2C(0)
    dht20 = DHT20(i2c)


def main():
    while True:
        temp = dht20.dht20_temperature()
        humid = dht20.dht20_humidity()

        #print("temper :    " + str(temper))
        #print("humidity : " + str(humidity))        
        print('Temp: {}'.format(temp)) 
        print('Humid: {}'.format(humid))
        
        utime.sleep(5) #wait 5 seconds


setup()
main()