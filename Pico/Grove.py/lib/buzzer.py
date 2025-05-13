##############################################################################
# Contains the class BUZZER, which is used to control the buzzer. 
# The class provides methods to play different notes and melodies. 
# The buzzer is connected to a PWM pin on the microcontroller.
# The code uses the PWM class from the machine module to control the    
# buzzer's frequency and duty cycle.
##############################################################################

from machine import I2C,Pin,PWM
from time import sleep

# Frequency values for musical notes
Freq = (30000,1046,1174,1318,1396,1567,1780,1975,2085)


class MUSIC:
    def __init__(self,pwm1):
        self.pwm = pwm1
                
    def music(self, number):
        self.pwm.freq(Freq[number])
        self.pwm.duty_u16(5000)


class BUZZER:
    def __init__(self):
        # DAC output (buzzer) connected to A1
        self.buzzer = PWM(Pin(27))


    def soundOff(self):    
        self.buzzer.duty_u16(0)

    # Predefined sound for OK event
    def soundOK(self):
        self.buzzer.duty_u16(10000)
        self.buzzer.freq(1000)
        sleep(0.1)
        self.buzzer.freq(2000)
        sleep(0.1)
        self.buzzer.freq(3000)
        sleep(0.1)    
        self.soundOff()

    # Predefined sound for error event
    def soundError(self):
        self.buzzer.freq(2000)
        self.buzzer.duty_u16(10000)
        sleep(0.1)
        self.buzzer.freq(1000)
        sleep(0.2)
        self.soundOff()   


    def do(self, duration=0.5):
        self.buzzer.freq(1046) #DO
        self.buzzer.duty_u16(1000)
        sleep(duration)
        self.soundOff()


    def re(self, duration=0.5):
        self.buzzer.freq(1175) #RE
        self.buzzer.duty_u16(1000)
        sleep(duration)        
        self.soundOff()


    def mi(self, duration=0.5):
        self.buzzer.freq(1318) #MI
        self.buzzer.duty_u16(1000)
        sleep(duration)
        self.soundOff()


    def fa(self, duration=0.5):
        self.buzzer.freq(1397) #FA
        self.buzzer.duty_u16(1000)
        sleep(duration)
        self.soundOff()


    def sol(self, duration=0.5):
        self.buzzer.freq(1568) #SO
        self.buzzer.duty_u16(1000) 
        sleep(duration)
        self.soundOff()


    def la(self, duration=0.5):
        self.buzzer.freq(1760) #LA
        self.buzzer.duty_u16(1000)
        sleep(duration)
        self.soundOff()


    def si(self, duration=0.5):
        self.buzzer.freq(1967) #SI
        self.buzzer.duty_u16(1000)
        sleep(duration)
        self.soundOff()





