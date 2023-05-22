from machine import Pin, I2C, ADC, PWM
from time import sleep

adc = ADC(2) #ADC输入（旋钮电位器）接A0
pwm = PWM(Pin(27))#DAC输出（蜂鸣器）接A1

while True:
    # Lees waarde van knop uit
    val = adc.read_u16()
    
    #Indien meer dan 300, pas de frequentie aan
    if val > 300:
        pwm.freq(int(val/30))
        pwm.duty_u16(1000)
    else:
        # Buzzer uit
        pwm.duty_u16(0)
    
