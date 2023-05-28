from machine import Pin, PWM
from time import sleep
from buzzer import BUZZER


def main():
    buzzer = BUZZER()
    buzzer.do()


main()