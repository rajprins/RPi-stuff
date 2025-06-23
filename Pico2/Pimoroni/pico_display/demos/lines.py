import math
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565

# Set up the display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB565)

#240x135
WIDTH, HEIGHT = display.get_bounds()

R=100
G=180
B=255

for Y in range(0,HEIGHT):
    red = R
    green = G
    blue = B - Y
    print("Y-axis:", Y, "Red:", red, "Green:", green, "Blue:", blue)

    color = display.create_pen(red,green,blue)
    display.set_pen(color)
    display.line(0,Y,WIDTH,Y)


display.update()





