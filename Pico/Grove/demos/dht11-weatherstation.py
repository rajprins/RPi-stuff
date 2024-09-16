##############################################################################
# Weather Station. Requires:
# * Grove Shield,
# * Temperature & Humidity Sensor,
# * LCD
##############################################################################


from lcd1602 import LCD1602
from machine import I2C, Pin
from dht11 import DHT
import utime
import rp2


def setup():
    global dht, ic2, display

    dht = DHT(16)  # DHT11 temp sensor connected to port D18
    i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)  # Connect I2C
    display = LCD1602(i2c, 2, 16)  # Connect LCD module


def main():
    while True:
        if rp2.bootsel_button():  # BOOTSEL pressed
            print('BOOTSEL pressed')
            display.clear()
            utime.sleep(2)  # wait 2 seconds
        else:
            temp, humid = dht.readTempHumid()
            display.clear()  # clear the LCD so old text isn't visible
            display.print('Temp: {} C'.format(temp))
            display.setCursor(0, 1)  # go to line 2 of the LCD
            display.print('Humid: {} %'.format(humid))
            print('Temp: {}'.format(temp))
            print('Humid: {}'.format(humid))

            utime.sleep(5)  # wait 5 seconds


setup()
main()
