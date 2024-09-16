from ssd1306 import SSD1306_I2C
from dht11 import *
from machine import Pin, I2C
from time import sleep

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000)#oled 接i2c1口
oled = SSD1306_I2C(128, 64, i2c)
dht2 = DHT(18) #温湿度传感器接D18口


while True:  

    temp,humid = dht2.readTempHumid()#temp:温度 humid:湿度
    '''I2C口测试'''    
    ''' oled显示器测试'''
    oled.fill(0)#清屏
    oled.text("Temp:  " + str(temp),0,0)#第一行显示温度
    oled.text("Humid: " + str(humid),0,8)
    oled.show()
    #sleep(0.5)