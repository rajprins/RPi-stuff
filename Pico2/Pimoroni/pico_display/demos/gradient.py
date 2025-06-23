import math
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565,PEN_RGB888

# Set up the display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB565)

#240x135
WIDTH, HEIGHT = display.get_bounds()

R, G, B = 210, 210, 255

green = G
for Y in range(0,HEIGHT):
    red = R
    green = G - int(Y/4)
    blue = B - int(Y/2)

    print("Y-axis:", Y, "Red:", red, "Green:", green, "Blue:", blue)

    color = display.create_pen(red,green,blue)
    display.set_pen(color)
    display.line(0,Y,WIDTH,Y)


display.update()






