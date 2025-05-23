from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
from machine import Pin
import pngdec

global ROTATION

button_a = Pin(12, Pin.IN, Pin.PULL_UP)
button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_x = Pin(14, Pin.IN, Pin.PULL_UP)
button_y = Pin(15, Pin.IN, Pin.PULL_UP)

def display_image():
    # Create a PicoGraphics instance
    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB332, rotate=ROTATION)

    # Set the backlight so we can see it!
    display.set_backlight(1.0)
    
    # Create an instance of the PNG Decoder
    png = pngdec.PNG(display)
    
    # Set white background
    BG = display.create_pen(255, 255, 255)
    display.set_pen(BG)
    
    # Clear the screen
    display.clear()
    
    # Display PNG file
    png.open_file("org42-logo.png")
    png.decode(30, 0, scale=1)

    display.update()


### Main
ROTATION = 90
display_image()


while True:    
    if button_x.value() == 0:
        ROTATION = ROTATION + 90
        display_image()
    #endif
        
    pass
#end while
