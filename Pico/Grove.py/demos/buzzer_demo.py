##############################################################################
# MicroPython code for Grove Buzzer
# Requires the Grove Buzzer module, which is a simple piezo buzzer
# that can produce sound.
# The buzzer can be used to generate different tones and melodies.
#
# Depends on file buzzer.py
# The buzzer.py file contains the class BUZZER, which is used to control
# the buzzer. The class provides methods to play different notes and
# melodies. The buzzer is connected to a PWM pin on the microcontroller.
# The code uses the PWM class from the machine module to control the    
# buzzer's frequency and duty cycle.
##############################################################################

from machine import Pin, PWM
from time import sleep
from buzzer import BUZZER


def main():
    buzzer = BUZZER()
    buzzer.do()
    buzzer.re()
    buzzer.mi()
    buzzer.fa()
    buzzer.sol()
    buzzer.la()
    buzzer.si()

main()