import rp2
from machine import Pin

led = Pin("LED", Pin.OUT)

print(">>> Press BOOTSEL button to turn on the onboard LED <<<")

while True:
    # BOOTSEL pressed
    if rp2.bootsel_button():
        led.on()
    # BOOTSEL not pressed
    else:
        led.off()
