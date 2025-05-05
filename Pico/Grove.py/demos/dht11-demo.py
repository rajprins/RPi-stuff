##############################################################################
#
# MicroPython code for DHT11 temperature & humidity sensor
#
##############################################################################


from lcd1602 import LCD1602
from machine import I2C,Pin
from time import sleep
from dht11 import DHT
import utime


def setup():
    global dht
    dht = DHT(16) #DHT11 temp sensor connected to port D16


def main():
    while True:       
        temp,humid = dht.readTempHumid()
        print('Temp: {}'.format(temp)) 
        print('Humid: {}'.format(humid))
        
        utime.sleep(5) # wait 5 seconds


setup()
main()
