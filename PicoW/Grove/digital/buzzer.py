from machine import I2C,Pin,PWM
from time import sleep


Freq = (30000,1046,1174,1318,1396,1567,1780,1975,2085)

class MUSIC:
    def __init__(self,pwm1):
        self.pwm = pwm1
                
    def music(self, number):
        self.pwm.freq(Freq[number])
        self.pwm.duty_u16(5000)


class BUZZER:
    def __init__(self):
        # body of the construc
        # DAC output (buzzer) connected to A1
        global i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
        global buzzer = PWM(Pin(27))    


    def soundOff():    
        buzzer.duty_u16(0)


    def soundOK():
        buzzer.duty_u16(10000)
        buzzer.freq(1000)
        sleep(0.1)
        buzzer.freq(2000)
        sleep(0.1)
        buzzer.freq(3000)
        sleep(0.1)    
        soundOff()


    def soundError():
        buzzer.freq(2000)
        buzzer.duty_u16(10000)
        sleep(0.1)
        buzzer.freq(1000)
        sleep(0.2)
        soundOff()   


