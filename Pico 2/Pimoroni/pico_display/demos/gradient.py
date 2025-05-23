import math
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB565

# Set up the display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB565)

#240x135
WIDTH, HEIGHT = display.get_bounds()

R=165
G=180
B=255

for Y in range(0,HEIGHT):
    blue = B - Y
    green = G - int(Y/4)
    print("Y:", Y, " B:", blue)
    color = display.create_pen(165,green,blue)
    display.set_pen(color)
    display.line(0,Y,WIDTH,Y)


display.update()






