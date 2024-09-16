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
from machine import I2C,Pin
from time import sleep
from dht11 import DHT


def setup():
    global dht,ic2, display
    
    # DHT11 temp/humid sensor aansluiten op poort D18
    dht = DHT(16) 

    # LCD 1602 module aansluiten op I2C1
    i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000) # Connect I2C
    display = LCD1602(i2c, 2, 16) 


def main():
    i=0

    # Herhaal alles hieronder tot het programma gestopt wordt
    while True:
        
        i += 1
        
        # Temperatuur en vochtigheid uitlezen
        temp, humid = dht.readTempHumid()
        print('[{}]----------'.format(i))
        print('Temperatuur {} C'.format(temp))
        print('Vochtigheid {} %'.format(humid))
        
        # LCD scherm leegmaken
        display.clear()
        
        # Toon tekst op eerste regel van LCD scherm
        display.setCursor(0,0)

        # Toon temperatuur op het LCD scherm
        display.print('Temperatuur {} C'.format(temp))
        
        # Ga naar regel 2 van het LCD scherm
        display.setCursor(0,1)
        
        # Toon de vochtigheid op LCD scherm
        display.print('Vochtigheid {} %'.format(humid))

        # Wacht 5 seconden
        sleep(5)


setup()
main()
