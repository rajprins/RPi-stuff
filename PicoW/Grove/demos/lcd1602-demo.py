from lcd1602 import LCD1602
from machine import I2C,Pin
from time import sleep

i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)

# Grove 16x2 LCD
# Aansluiten op I2C1
display = LCD1602(i2c, 2, 16)

# Cursor naar eerste regel
display.home()
display.print('*RASPBERRY PICO*')

# Cursor naar volgende regel
display.setCursor(0, 1)
display.print('Hello world!')

