#!/usr/bin/env python

import time

from grove.display.jhd1802 import JHD1802

def main():
    # Grove - 16x2 LCD(White on Blue) connected to I2C port
    lcd = JHD1802()

    #cursor naar regel 1
    lcd.setCursor(0, 0)
    lcd.write('Hallo Sonja..')

    #cursor naar regel 2
    lcd.setCursor(1,0)
    lcd.write('Het werkt!!!')



if __name__ == '__main__':
    main()

