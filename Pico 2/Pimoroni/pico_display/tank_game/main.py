import math
import random
import utime
import machine
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565
from pimoroni import RGBLED
from tank import Tank
from shell import Shell
from terrain import Terrain

button_a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button_b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button_x = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button_y = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# Set up Display Pack and Display Pack 2.0
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB565, rotate=0)

# Set up the RGB LED For Display Pack and Display Pack 2.0
led = RGBLED(6, 7, 8)

# Screen brightness
display.set_backlight(1.0)

# Get screen dimenions
WIDTH, HEIGHT = display.get_bounds()

### Colour constants

# Sky color is light blue
SKY_COLOR = display.create_pen(165,182,255)

# Ground color is green
GND_COLOR = display.create_pen(9,84,5)     

# Tank 1 is blue
TANK_COLOR_P1 = display.create_pen(0, 0, 255)

# Tank 2 is red
TANK_COLOR_P2 = display.create_pen(255, 0, 0)

# Shell color is white
SHELL_COLOR = display.create_pen(255,255,255)

# Active text is white
TEXT_COLOR_ACTIVE = display.create_pen(255,255,255)

# Other text is black
TEXT_COLOR = display.create_pen(0,0,0)

# States are:
#   start - timed delay before start
#   player1 - waiting for player to set position
#   player1fire - player 1 fired
#   player2 - player 2 set position
#   player2fire - player 2 fired
#   game_over_1 / game_over_2 - show who won 1 = player 1 won etc.
game_state = "player1"

# switch button mode from angle to power
key_mode = "angle"

# Tank 1 = Left
tank1 = Tank(display, "left", TANK_COLOR_P1)

# Tank 2 = Right
tank2 = Tank(display, "right", TANK_COLOR_P2)

# Only fire one shell at a time, a single shell object can be used for both player 1 and player 2    
shell = Shell(display, SHELL_COLOR)

# Draw ground
ground = Terrain(display, GND_COLOR)


def run_game():
    global key_mode, game_state
    
    R=165
    G=180
    B=255

    while True:
        # Draw gradient background color as sky
        #display.set_pen(SKY_COLOR)
        #display.clear()
        for Y in range(0,HEIGHT):
            blue = B - Y
            green = G - int(Y/4)
            color = display.create_pen(165,green,blue)
            display.set_pen(color)
            display.line(0,Y,WIDTH,Y)
        #endloop
        
        display.set_pen(TANK_COLOR_P1)
        
        # Draw terrain
        ground.draw()
        
        # Draw tank 1
        tank1.draw ()
        
        # Draw tank 2
        tank2.draw ()
        
        # Refresh screen
        display.update()
        
        if (game_state == "player1fire" or game_state == "player2fire"):
            shell.draw()

        display.set_pen(TEXT_COLOR)
        
        # Display score and status info for player 1
        if (game_state == "player1" or game_state == "player1fire"):
            # Set onboard LED to color blue
            led.set_rgb(0, 0, 255)
            # Set display
            display.set_pen(TANK_COLOR_P1)
            display.text("PLAYER1", 5, 5, 240, 2)
            display.set_pen(TEXT_COLOR)
            
            # When POWER is selected
            if (key_mode == "power"):
                display.set_pen(TEXT_COLOR_ACTIVE)
            display.text("PWR "+str(tank1.get_gun_power())+"%", 85, 5, 240, 2)
            
            # When ANGLE is selected
            if (key_mode == "angle"):
                display.set_pen(TEXT_COLOR_ACTIVE)
            else:
                display.set_pen(TEXT_COLOR)
            display.text("ANG "+str(tank1.get_gun_angle()), 170, 5, 240, 2)


        # Display score and status info for player 2
        if (game_state == "player2" or game_state == "player2fire"):
            # Set onboard LED to color blue
            led.set_rgb(255, 0, 0)
            # Set display            
            display.set_pen(TANK_COLOR_P2)
            display.text("PLAYER2", 5, 5, 240, 2)
            display.set_pen(TEXT_COLOR)

            # If POWER is selected
            if (key_mode == "power"):
                display.set_pen(TEXT_COLOR_ACTIVE)
            display.text("PWR "+str(tank2.get_gun_power())+"%", 85, 5, 240, 2)
            
            # If ANGLE is selected
            if (key_mode == "angle"):
                display.set_pen(TEXT_COLOR_ACTIVE)
            else:
                display.set_pen(TEXT_COLOR)
            display.text("ANG "+str(tank2.get_gun_angle()), 170, 5, 240, 2)

            
        # Display text if Player1 wins
        if (game_state == "game_over_1"):
            # Simulate text shadow by drawing the same text twice in different colors
            display.set_pen(TEXT_COLOR)
            display.text("Game Over", 44, 24, 240, 3)
            display.text("Player 1 wins", 24, 54, 240, 3)
            display.text("Press <B>", 44, 94, 240, 3)
            # Simulate text shadow by drawing the same text twice in different colors, offset by 4 pixels
            display.set_pen(TEXT_COLOR_ACTIVE)
            display.text("Game Over", 40, 20, 240, 3)
            display.text("Player 1 wins", 20, 50, 240, 3)
            display.text("Press <B>", 40, 90, 240, 3)
            
        # Display text if Player 2 wins
        if (game_state == "game_over_2"):
            # Simulate text shadow by drawing the same text twice in different colors
            display.set_pen(TEXT_COLOR)
            display.text("Game Over", 44, 24, 240, 3)
            display.text("Player 2 wins", 24, 54, 240, 3)
            display.text("Press <B>", 44, 94, 240, 3)
            # Simulate text shadow by drawing the same text twice in different colors, offset by 4 pixels
            display.set_pen(TEXT_COLOR_ACTIVE)
            display.text("Game Over", 40, 20, 240, 3)
            display.text("Player 2 wins", 20, 50, 240, 3)
            display.text("Press <B>", 40, 90, 240, 3)
            
        # Redraw screen
        display.update()


        ## Update methods
        # Only read keyboard in certain states
        
        # Player1's turn
        if (game_state == 'player1'):
            player1_fired = player_keyboard("left")
            if (player1_fired == True):
                # Set shell position to end of gun
                # Use gun_positions so we can get start position 
                gun_positions = tank1.calc_gun_positions ()
                start_shell_pos = (gun_positions[3][0],gun_positions[3][1]+2)
                shell.set_start_position(start_shell_pos)
                shell.set_current_position(start_shell_pos)
                game_state = 'player1fire'
                shell.set_angle(math.radians (tank1.get_gun_angle()))
                shell.set_power(tank1.get_gun_power() / 40)
                shell.set_time(0)
        
        # Player1 fired shot
        if (game_state == 'player1fire'):
            shell.update_shell_position ("left")
            # shell value is whether the shell is inflight, hit or missed
            shell_value = detect_hit("left")
            # shell_value 20 is if other tank hit
            if (shell_value >= 20):
                game_state = 'game_over_1'
            # 10 is offscreen and 11 is hit ground, both indicate missed
            elif (shell_value >= 10):
                print("Player 1 missed")
                # reset key mode to angle
                key_mode = "angle"
                # Turn to Player2
                game_state = 'player2'


        # Player2's turn
        if (game_state == 'player2'):
            player2_fired = player_keyboard("right")
            if (player2_fired == True):
                # Set shell position to end of gun
                # Use gun_positions so we can get start position 
                gun_positions = tank2.calc_gun_positions ()
                start_shell_pos = (gun_positions[3][0],gun_positions[3][1]+2)
                shell.set_start_position(start_shell_pos)
                shell.set_current_position(start_shell_pos)
                game_state = 'player2fire'
                shell.set_angle(math.radians (tank2.get_gun_angle()))
                shell.set_power(tank2.get_gun_power() / 40)
                shell.set_time(0)
                
        # Player2 fired a shot
        if (game_state == 'player2fire'):
            shell.update_shell_position ("right")
            # shell value is whether the shell is inflight, hit or missed
            shell_value = detect_hit("right")
            # shell_value 20 is if other tank hit
            if (shell_value >= 20):
                game_state = 'game_over_2'
            # 10 is offscreen and 11 is hit ground, both indicate missed
            elif (shell_value >= 10):
                print("Player 2 missed")
                # reset key mode to angle
                key_mode = "angle"                
                # Turn to player1
                game_state = 'player1'

        
        # Hit
        if (game_state == 'game_over_1' or game_state == 'game_over_2'):
            # Allow space key or left-shift (picade) to continue
            if (button_b.value() == 0) :
                # Reset position of tanks and terrain
                setup()


# Reset
def setup():
    global game_state, key_mode
    
    # reset key mode to angle
    key_mode = "angle"
    ground.setup()
    
    # Get positions of tanks from ground generator
    tank1.set_position(ground.get_tank1_position())
    tank2.set_position(ground.get_tank2_position())
    
    game_state = "player1"
    print("Active player:", game_state)
    
    
    
# Detects if the shell has hit something. 

# Return 0 for in-flight, 
# 1 for offscreen temp (too high), 
# 10 for offscreen permanent (too far), 
# 11 for hit ground, 
# 20 for hit other tank
def detect_hit (left_right):
    (shell_x, shell_y) = shell.get_current_position()
    # Add offset (3 pixels)
    # offset left/right depending upon direction of fire
    if (left_right == "left"):      
        shell_x += 2
    else:
        shell_x -= 2
    shell_y += 2
    offset_position = (math.floor(shell_x), math.floor(shell_y))
    
    # Check whether it's off the screen 
    # may be temporary if just y axis, permanent if x
    if (shell_x > WIDTH or shell_x <= 0 or shell_y >= HEIGHT):
        return 10
    if (shell_y < 1):
        # special case if gone beyond size of screen then that's too far
        if (shell_y < 0-HEIGHT):
            return 10
        return 1
        
    # check to see if it's hit a tank
    
    # get x and y for rect covering tank
    tank1_rect = tank1.get_rect()
    tank2_rect = tank2.get_rect()
    
    # If gone below bottom of screen - hit ground
    if (shell_y >= HEIGHT):
        return 11
    
    # If hit tank 1
    if (left_right == 'right' and
        shell_x >= tank1_rect[0] and
        shell_x <= tank1_rect[2] and
        shell_y >= tank1_rect[1] and
        shell_y <= tank1_rect[3]):
        print("*** Player 2 hit Tank 1 ***")
        return 20

    # If hit tank 2
    if (left_right == 'left' and
            shell_x >= tank2_rect[0] and
            shell_x <= tank2_rect[2] and
            shell_y >= tank2_rect[1] and
            shell_y <= tank2_rect[3]):
        print("*** Player 1 hit Tank 2 ***")
        return 20

    if (ground.is_ground(int(shell_x), int(shell_y))):
        return 11
    
    return 0
    

# Handles keyboard for players
# Although named keyboard (consistancy with pygame zero version) - for the pico this refers to buttons
# If player has hit fire key (space) then returns True
# Otherwise changes angle of gun if applicable and returns False
def player_keyboard(left_right):
    global key_mode
    
    # change key_mode between angle and power using B button
    if (button_b.value() == 0) :
        if key_mode == "angle":
            print(game_state, "- Switched to POWER")
            key_mode = "power"
        else:
            print(game_state, "- Switched to ANGLE")
            key_mode = "angle"
        # add delay to prevent accidental double press
        utime.sleep(0.5)
    
    # A button is fire
    if (button_a.value() == 0) :
        print(game_state, "- Shot fired")
        return True
    
    # Up moves firing angle upwards or increase power
    if (button_x.value() == 0) :
        #print ("X pressed")
        if (key_mode == "angle" and left_right == 'left'):
            print(game_state, "- Pressed X: angle up")
            tank1.change_gun_angle(5)
        elif (key_mode == "angle" and left_right == 'right'):
            print(game_state, "- Pressed X: angle up")
            tank2.change_gun_angle(5)
        elif (key_mode == "power" and left_right == 'left'):
            print(game_state, "- Pressed X: power up")
            tank1.change_gun_power(5)
        elif (key_mode == "power" and left_right == 'right'):
            print(game_state, "- Pressed X: power up")
            tank2.change_gun_power(5)
    # Down moves firing angle downwards or decrease power
    if (button_y.value() == 0) :
        if (key_mode == "angle" and left_right == 'left'):
            print(game_state, "- Pressed Y: angle down")
            tank1.change_gun_angle(-5)
        elif (key_mode == "angle" and left_right == 'right'):
            print(game_state, "- Pressed Y: angle down")
            tank2.change_gun_angle(-5)
        elif (key_mode == "power" and left_right == 'left'):
            print(game_state, "- Pressed Y: power down")
            tank1.change_gun_power(-5)
        elif (key_mode == "power" and left_right == 'right'):
            print(game_state, "- Pressed Y: power down")
            tank2.change_gun_power(-5)

    return False


# Returns as list
def get_display_bytes (x, y):
    buffer_pos = (x*2) + (y*WIDTH*2)
    byte_list = [display_buffer[buffer_pos], display_buffer[buffer_pos+1]]
    return (byte_list)


def color_to_bytes (color):
    r, g, b = color
    bytes = [0,0]
    bytes[0] = r & 0xF8
    bytes[0] += (g & 0xE0) >> 5
    bytes[1] = (g & 0x1C) << 3
    bytes[1] += (b & 0xF8) >> 3
    
    return bytes


### MAIN ###
setup()
run_game()



