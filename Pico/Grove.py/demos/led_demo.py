from machine import Pin

button = Pin(18, Pin.IN, Pin.PULL_UP)
button.irq(lambda pin: InterruptsButton(),Pin.IRQ_FALLING)
led = Pin(16, Pin.OUT)
tmp = 0


def InterruptsButton():
    global tmp
    tmp = ~tmp
    led.value(tmp)


while True:  
    pass