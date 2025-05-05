##############################################################################
# Eenvoudig weerstation op basis van Raspberry Pico en temperatuur sensor    #
# Benodigheden:                                                              #
#   - Raspberry Pi Pico                                                      #
#   - USB kabeltje                                                           #
#   - Grove Shield                                                           #
#   - Temperatuur sensor                                                     #
#   - 16x02 LCD                                                              #
##############################################################################

from lcd1602 import LCD1602
from machine import I2C, Pin
from dht11 import DHT
from time import sleep
import rp2


def setup():
    global dht,ic2, display
    # DHT11 temp/humid sensor aansluiten op poort D16
    dht = DHT(16) 
    # I2C poort selecteren
    i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000) # Connect I2C
    # LCD 1602 module aansluiten op I2C1
    display = LCD1602(i2c, 2, 16) 


def main():
    while True:
        # Indien BOOTSEL is ingedrukt
        if rp2.bootsel_button():
            print('BOOTSEL pressed')
            # LCD scherm leegmaken
            display.clear()
            # Wacht 2 seconden
            sleep(2)
        else:
            # Temperatuur en vochtigheid uitlezen
            temp, humid = dht.readTempHumid()
            # LCD scherm leegmaken
            display.clear()
            # Cursor naar eerste regel van LCD scherm
            display.setCursor(0,0)
            # Toon temperatuur op het LCD scherm
            display.print('Temperatuur {} C'.format(temp))
            # Ga naar regel 2 van het LCD scherm
            display.setCursor(0,1)
            # Toon de vochtigheid op LCD scherm
            display.print('Vochtigheid {} %'.format(humid))
            # Wacht 5 seconden
            sleep(5)            
        #end if
    #end while
#end main()


setup()
main()
