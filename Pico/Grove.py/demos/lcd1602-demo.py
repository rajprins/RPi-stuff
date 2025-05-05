from lcd1602 import LCD1602
from machine import I2C,Pin

i2c0 = I2C(0,scl=Pin(9), sda=Pin(8), freq=400000)
i2c1 = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)

# Grove 16x2 LCD, aangesloten op poort I2Cx
display = LCD1602(i2c0)

# Eerste regel
display.printLine1('*RASPBERRY PICO*')

# Tweede regel
display.printLine2('Hello, World!')

