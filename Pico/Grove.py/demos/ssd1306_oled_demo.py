from ssd1306 import SSD1306_I2C
from dht11 import *
from machine import Pin, I2C
from time import sleep

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000)
oled = SSD1306_I2C(128, 64, i2c)
dht2 = DHT(18)


while True:  
    temp,humid = dht2.readTempHumid()
    oled.fill(0)
    oled.text("Temp:  " + str(temp),0,0)
    oled.text("Humid: " + str(humid),0,8)
    oled.show()
    #sleep(0.5)