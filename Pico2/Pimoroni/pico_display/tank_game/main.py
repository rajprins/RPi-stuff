################################################################################
# https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics#pico-graphics-
################################################################################

import math
import random
import utime
import machine
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565
from pimoroni import RGBLED
from tank import Tank
from shell import Shell
from terrain import Terrain

# --- Hardware Setup ---
button_a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button_b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button_x = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button_y = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

#display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB888, rotate=0)
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB565, rotate=0)
led = RGBLED(6, 7, 8)
display.set_backlight(1.0)
WIDTH, HEIGHT = display.get_bounds()

# --- Color Constants ---
SKY_COLOR = display.create_pen(165,182,255)
GND_COLOR = display.create_pen(9,84,5)
TANK_COLOR_P1 = display.create_pen(0, 0, 255)
TANK_COLOR_P2 = display.create_pen(255, 0, 0)
SHELL_COLOR = display.create_pen(255,255,255)
TEXT_COLOR_ACTIVE = display.create_pen(255,255,255)
TEXT_COLOR = display.create_pen(0,0,0)

# --- Utility Functions ---
def draw_background(display, width, height):
    R, G, B = 165, 180, 255
    for Y in range(0, height):
        red = R
        green = G - int(Y / 4)
        blue = B - Y
        color = display.create_pen(red, green, blue)
        display.set_pen(color)
        display.line(0, Y, width, Y)

# --- Game Class ---
class Game:
    def __init__(self, display, led):
        self.display = display
        self.led = led
        self.width, self.height = display.get_bounds()
        self.terrain = Terrain(display, GND_COLOR)
        self.tank1 = Tank(display, "left", TANK_COLOR_P1)
        self.tank2 = Tank(display, "right", TANK_COLOR_P2)
        self.shell = Shell(display, SHELL_COLOR)
        self.game_state = "player1"
        self.key_mode = "angle"
        self.setup()

    def setup(self):
        self.key_mode = "angle"
        self.terrain.setup()
        self.tank1.reset()
        self.tank2.reset()
        self.tank1.set_position(self.terrain.get_tank1_position())
        self.tank2.set_position(self.terrain.get_tank2_position())
        self.game_state = "player1"
        print("Active player:", self.game_state)

    # Detects successful hit based on shell and enemy tank coordinates
    def detect_hit(self, left_right):
        shell_x, shell_y = self.shell.get_current_position()
        shell_x += 2 if left_right == "left" else -2
        shell_y += 2
        if (shell_x > self.width or shell_x <= 0 or shell_y >= self.height):
            return 10
        if (shell_y < 1):
            if (shell_y < 0 - self.height):
                return 10
            return 1
        tank1_rect = self.tank1.get_rect()
        tank2_rect = self.tank2.get_rect()
        if (shell_y >= self.height):
            return 11
        if (left_right == 'right' and
            tank1_rect[0] <= shell_x <= tank1_rect[2] and
            tank1_rect[1] <= shell_y <= tank1_rect[3]):
            print("*** Player 2 hit Tank 1 ***")
            return 20
        if (left_right == 'left' and
            tank2_rect[0] <= shell_x <= tank2_rect[2] and
            tank2_rect[1] <= shell_y <= tank2_rect[3]):
            print("*** Player 1 hit Tank 2 ***")
            return 20
        if (self.terrain.is_ground(int(shell_x), int(shell_y))):
            return 11
        return 0

    def key_pressed(self, left_right):
        # Switch key mode
        if button_b.value() == 0:
            self.key_mode = "power" if self.key_mode == "angle" else "angle"
            print(self.game_state, "- Switched to", self.key_mode.upper())
            utime.sleep(0.5)
        # Fire
        if button_a.value() == 0:
            print(self.game_state, "- Shot fired")
            return True
        # Up/Down for angle/power
        if button_x.value() == 0:
            if self.key_mode == "angle":
                tank = self.tank1 if left_right == 'left' else self.tank2
                tank.change_gun_angle(5)
                print(self.game_state, "- Pressed X, angle up:", tank.get_gun_angle(), 'degrees')
            else:
                tank = self.tank1 if left_right == 'left' else self.tank2
                tank.change_gun_power(5)
                print(self.game_state, "- Pressed X, power up:", tank.get_gun_power(), 'degrees')
        if button_y.value() == 0:
            if self.key_mode == "angle":
                tank = self.tank1 if left_right == 'left' else self.tank2
                tank.change_gun_angle(-5)
                print(self.game_state, "- Pressed Y, angle down:", tank.get_gun_angle(), 'degrees')
            else:
                tank = self.tank1 if left_right == 'left' else self.tank2
                tank.change_gun_power(-5)
                print(self.game_state, "- Pressed Y, power down:", tank.get_gun_power(), 'degrees')
        return False


    def draw_ui(self):
        # Draw background (sky)
        draw_background(self.display, self.width, self.height)
        # Draw terrain
        self.terrain.draw()
        # Draw tanks
        #self.display.set_pen(TANK_COLOR_P1)
        self.tank1.draw()
        self.tank2.draw()
        if self.game_state in ("player1fire", "player2fire"):
            self.shell.draw()

        self.display.set_font("bitmap8")
        self.display.set_pen(TEXT_COLOR)
        # Player 1 indicator
        if self.game_state in ("player1", "player1fire"):
            # set color of onboard LED to blue to indicate player 1's turn
            self.led.set_rgb(0, 0, 5)
            self.display.set_pen(TANK_COLOR_P1)
            self.display.text("PLAYER1", 5, 3, 240, 2)
            self._draw_power_angle(self.tank1)
        # Player 2 indicator
        if self.game_state in ("player2", "player2fire"):
            # set color of onboard LED to red to indicate player 2's turn
            self.led.set_rgb(5, 0, 0)
            self.display.set_pen(TANK_COLOR_P2)
            self.display.text("PLAYER2", 5, 3, 240, 2)
            self._draw_power_angle(self.tank2)
        # Game over screens
        if self.game_state == "game_over_1":
            self._draw_game_over("Player 1 wins")
        if self.game_state == "game_over_2":
            self._draw_game_over("Player 2 wins")
        self.display.update()


    def _draw_power_angle(self, tank):
        # Power
        if self.key_mode == "power":
            self.display.set_pen(TEXT_COLOR)
            self.display.text(f"PWR {tank.get_gun_power()}%", 86, 4, 240, 2)
            self.display.set_pen(TEXT_COLOR_ACTIVE)
            self.display.text(f"PWR {tank.get_gun_power()}%", 85, 3, 240, 2)
        else:
            self.display.set_pen(TEXT_COLOR)
            self.display.text(f"PWR {tank.get_gun_power()}%", 85, 3, 240, 2)
        # Angle
        if self.key_mode == "angle":
            self.display.set_pen(TEXT_COLOR)
            self.display.text(f"ANG {tank.get_gun_angle()}", 171, 4, 240, 2)
            self.display.set_pen(TEXT_COLOR_ACTIVE)
            self.display.text(f"ANG {tank.get_gun_angle()}", 170, 3, 240, 2)
        else:
            self.display.set_pen(TEXT_COLOR)
            self.display.text(f"ANG {tank.get_gun_angle()}", 170, 3, 240, 2)

    def _draw_game_over(self, winner_text):
        self.display.set_pen(TEXT_COLOR)
        self.display.text("Game Over", 43, 23, 240, 3)
        self.display.text(winner_text, 23, 53, 240, 3)
        self.display.text("Press <B>", 43, 93, 240, 3)
        self.display.set_pen(TEXT_COLOR_ACTIVE)
        self.display.text("Game Over", 40, 20, 240, 3)
        self.display.text(winner_text, 20, 50, 240, 3)
        self.display.text("Press <B>", 40, 90, 240, 3)

    def run(self):
        while True:
            self.draw_ui()
            # Player 1 turn
            if self.game_state == 'player1':
                if self.key_pressed("left"):
                    gun_positions = self.tank1.calc_gun_positions()
                    start_shell_pos = (gun_positions[3][0], gun_positions[3][1]+2)
                    self.shell.set_start_position(start_shell_pos)
                    self.shell.set_current_position(start_shell_pos)
                    self.game_state = 'player1fire'
                    self.shell.set_angle(math.radians(self.tank1.get_gun_angle()))
                    self.shell.set_power(self.tank1.get_gun_power() / 40)
                    self.shell.set_time(0)
            # Player 1 fire
            elif self.game_state == 'player1fire':
                self.shell.update_shell_position("left")
                shell_value = self.detect_hit("left")
                if shell_value >= 20:
                    self.game_state = 'game_over_1'
                elif shell_value >= 10:
                    print("player1 - Missed")
                    self.key_mode = "angle"
                    self.game_state = 'player2'
            # Player 2 turn
            elif self.game_state == 'player2':
                if self.key_pressed("right"):
                    gun_positions = self.tank2.calc_gun_positions()
                    start_shell_pos = (gun_positions[3][0], gun_positions[3][1]+2)
                    self.shell.set_start_position(start_shell_pos)
                    self.shell.set_current_position(start_shell_pos)
                    self.game_state = 'player2fire'
                    self.shell.set_angle(math.radians(self.tank2.get_gun_angle()))
                    self.shell.set_power(self.tank2.get_gun_power() / 40)
                    self.shell.set_time(0)
            # Player 2 fire
            elif self.game_state == 'player2fire':
                self.shell.update_shell_position("right")
                shell_value = self.detect_hit("right")
                if shell_value >= 20:
                    self.game_state = 'game_over_2'
                elif shell_value >= 10:
                    print("player2 - Missed")
                    self.key_mode = "angle"
                    self.game_state = 'player1'
            # Game over
            elif self.game_state in ('game_over_1', 'game_over_2'):
                if button_b.value() == 0:
                    self.setup()

# --- Main Entry Point ---
if __name__ == "__main__":
    game = Game(display, led)
    game.run()

