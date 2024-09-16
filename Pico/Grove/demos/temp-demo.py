import rp2
from machine import I2C, Pin
from dht11 import DHT11
from lcd1602 import LCD1602

def setup():
    global led
    global display
    
    i2c0 = I2C(0,scl=Pin(9), sda=Pin(8), freq=400000)
    i2c1 = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
    
    led = Pin("LED", Pin.OUT)
    # Grove 16x2 LCD, aangesloten op poort I2Cx
    display = LCD1602(i2c0)
    
    pin = Pin(2, Pin.OUT, Pin.PULL_DOWN)
    dht11 = DHT11(pin)


def main():
    print(">>> Press BOOTSEL button to check the temperature <<<")

    while True:
        # BOOTSEL pressed
        if rp2.bootsel_button():
            led.on()
        # BOOTSEL not pressed
        else:
            led.off()


setup()
main()