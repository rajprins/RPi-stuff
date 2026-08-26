################################################################################
# https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics#pico-graphics-
################################################################################

import math
import utime
import machine
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565
from pimoroni import RGBLED
from tank import Tank
from shell import Shell
from terrain import Terrain

# --- Hardware Setup ---
class Button:
    """Edge-triggered button with optional hold-to-repeat.

    pressed() returns True exactly once per physical press (on the
    falling edge), so a short tap can never register multiple times.
    If `repeat=(initial_ms, repeat_ms)` is given, holding the button
    fires again after `initial_ms` and then every `repeat_ms`.
    """

    def __init__(self, pin, repeat=None):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.repeat = repeat
        self.was_down = False
        self.next_repeat = 0

    def pressed(self):
        down = self.pin.value() == 0
        if not down:
            self.was_down = False
            return False
        now = utime.ticks_ms()
        if not self.was_down:
            # New press (falling edge)
            self.was_down = True
            if self.repeat:
                self.next_repeat = utime.ticks_add(now, self.repeat[0])
            return True
        # Held down: auto-repeat if configured
        if self.repeat and utime.ticks_diff(now, self.next_repeat) >= 0:
            self.next_repeat = utime.ticks_add(now, self.repeat[1])
            return True
        return False


# X/Y auto-repeat: first repeat after 250 ms, then every 100 ms while held.
button_a = Button(12)
button_b = Button(13)
button_x = Button(14, repeat=(250, 100))
button_y = Button(15, repeat=(250, 100))

#display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB888, rotate=0)
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB565, rotate=0)
led = RGBLED(6, 7, 8)
display.set_backlight(1.0)
WIDTH, HEIGHT = display.get_bounds()

# --- Color Constants ---
GND_COLOR = display.create_pen(9,84,5)
TANK_COLOR_P1 = display.create_pen(0, 0, 255)
TANK_COLOR_P2 = display.create_pen(255, 0, 0)
SHELL_COLOR = display.create_pen(255,255,255)
TEXT_COLOR_ACTIVE = display.create_pen(255,255,255)
TEXT_COLOR = display.create_pen(0,0,0)

# Precompute the sky gradient as bands of rows sharing one pen.
# Creating pens is relatively expensive on the Pico, so doing it once at
# startup (instead of every frame) is a big performance win. Grouping
# rows into 4-row bands cuts draw calls ~4x; the color step per band is
# below what RGB565 can resolve, so it looks identical.
SKY_BAND_HEIGHT = 4
_R, _G, _B = 165, 180, 255
SKY_GRADIENT_BANDS = [
    (Y, display.create_pen(_R, _G - (Y // 4), _B - Y))
    for Y in range(0, HEIGHT, SKY_BAND_HEIGHT)
]

# --- Utility Functions ---
def draw_background(display, width, height):
    # Draw the precomputed sky gradient, one rectangle per band.
    for y, pen in SKY_GRADIENT_BANDS:
        display.set_pen(pen)
        display.rectangle(0, y, width, SKY_BAND_HEIGHT)

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
        # Dirty flag: only push a frame to the display when something has
        # actually changed. Constantly re-sending the full framebuffer over
        # SPI (unsynced with the panel refresh) causes visible flicker.
        self.dirty = True
        self.setup()

    def setup(self, first_player="player1"):
        self.key_mode = "angle"
        self.terrain.setup()
        self.tank1.reset()
        self.tank2.reset()
        self.tank1.set_position(self.terrain.get_tank1_position())
        self.tank2.set_position(self.terrain.get_tank2_position())
        self.game_state = first_player
        self.dirty = True
        print("Active player:", self.game_state)

    # Classifies a shell position (see _detect_hit_at for the codes).
    def detect_hit(self, left_right):
        shell_x, shell_y = self.shell.get_current_position()
        return self._detect_hit_at(shell_x, shell_y, left_right)

    def _detect_hit_at(self, shell_x, shell_y, left_right):
        # Offset to the shell's visual center
        shell_x += 2 if left_right == "left" else -2
        shell_y += 2
        # Off the sides: miss
        if shell_x > self.width or shell_x <= 0:
            return 10
        # Above the screen: still flying (unless absurdly high)
        if shell_y < 1:
            if shell_y < 0 - self.height:
                return 10
            return 1
        # Below the screen: counts as hitting the ground
        if shell_y >= self.height:
            return 11
        # Enemy tank bounding box
        if left_right == 'right':
            rect = self.tank1.get_rect()
        else:
            rect = self.tank2.get_rect()
        if (rect[0] <= shell_x <= rect[2] and
                rect[1] <= shell_y <= rect[3]):
            print("*** Player 2 hit Tank 1 ***" if left_right == 'right'
                  else "*** Player 1 hit Tank 2 ***")
            return 20
        if self.terrain.is_ground(int(shell_x), int(shell_y)):
            return 11
        return 0

    # Checks the shell's path from its previous to current position,
    # sampling intermediate points so a fast shell (up to ~15 px per
    # update at high power) cannot tunnel through a 14 px tall tank
    # or a thin ridge between two frames.
    def detect_hit_swept(self, left_right):
        x0, y0 = self.shell.get_previous_position()
        x1, y1 = self.shell.get_current_position()
        dx = x1 - x0
        dy = y1 - y0
        # One sample every ~4 px of travel, minimum 1 (the endpoint)
        dist = abs(dx) + abs(dy)
        steps = max(1, int(dist // 4))
        for i in range(1, steps + 1):
            t = i / steps
            result = self._detect_hit_at(x0 + dx * t, y0 + dy * t, left_right)
            if result != 0 and result != 1:
                return result
        # Report the endpoint state (0 in flight / 1 above screen)
        return self._detect_hit_at(x1, y1, left_right)

    def key_pressed(self, left_right):
        # The active tank is the same for every branch below, so select it once.
        tank = self.tank1 if left_right == 'left' else self.tank2
        # Switch key mode (edge-triggered: fires once per press, no sleep needed)
        if button_b.pressed():
            self.key_mode = "power" if self.key_mode == "angle" else "angle"
            print(self.game_state, "- Switched to", self.key_mode.upper())
            self.dirty = True
        # Fire
        if button_a.pressed():
            print(self.game_state, "- Shot fired")
            return True
        # Up/Down for angle/power (edge-triggered with hold-to-repeat)
        if button_x.pressed():
            if self.key_mode == "angle":
                tank.change_gun_angle(5)
                print(self.game_state, "- Pressed X, angle up:", tank.get_gun_angle(), 'degrees')
            else:
                tank.change_gun_power(5)
                print(self.game_state, "- Pressed X, power up:", tank.get_gun_power(), '%')
            self.dirty = True
        if button_y.pressed():
            if self.key_mode == "angle":
                tank.change_gun_angle(-5)
                print(self.game_state, "- Pressed Y, angle down:", tank.get_gun_angle(), 'degrees')
            else:
                tank.change_gun_power(-5)
                print(self.game_state, "- Pressed Y, power down:", tank.get_gun_power(), '%')
            self.dirty = True
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
        pwr_text = f"PWR {tank.get_gun_power()}%"
        ang_text = f"ANG {tank.get_gun_angle()}"
        # Power (active mode gets a drop shadow + white highlight)
        if self.key_mode == "power":
            self.display.set_pen(TEXT_COLOR)
            self.display.text(pwr_text, 86, 4, 240, 2)
            self.display.set_pen(TEXT_COLOR_ACTIVE)
            self.display.text(pwr_text, 85, 3, 240, 2)
        else:
            self.display.set_pen(TEXT_COLOR)
            self.display.text(pwr_text, 85, 3, 240, 2)
        # Angle
        if self.key_mode == "angle":
            self.display.set_pen(TEXT_COLOR)
            self.display.text(ang_text, 171, 4, 240, 2)
            self.display.set_pen(TEXT_COLOR_ACTIVE)
            self.display.text(ang_text, 170, 3, 240, 2)
        else:
            self.display.set_pen(TEXT_COLOR)
            self.display.text(ang_text, 170, 3, 240, 2)

    def _draw_game_over(self, winner_text):
        self.display.set_pen(TEXT_COLOR)
        self.display.text("Game Over", 43, 23, 240, 3)
        self.display.text(winner_text, 23, 53, 240, 3)
        self.display.text("Press <B>", 43, 93, 240, 3)
        self.display.set_pen(TEXT_COLOR_ACTIVE)
        self.display.text("Game Over", 40, 20, 240, 3)
        self.display.text(winner_text, 20, 50, 240, 3)
        self.display.text("Press <B>", 40, 90, 240, 3)

    # Target loop delay in seconds. Caps the frame/input rate so button
    # presses (X/Y) don't repeat too fast to control, while keeping shell
    # animation smooth.
    FRAME_DELAY = 0.02

    def run(self):
        while True:
            # Only redraw and push the framebuffer when something changed.
            # Re-sending an identical frame every loop iteration makes the
            # panel flicker and wastes CPU/SPI bandwidth.
            if self.dirty:
                self.draw_ui()
                self.dirty = False
            utime.sleep(self.FRAME_DELAY)
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
                    self.dirty = True
            # Player 1 fire
            elif self.game_state == 'player1fire':
                self.shell.update_shell_position("left")
                self.dirty = True  # shell moved, animate it
                shell_value = self.detect_hit_swept("left")
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
                    self.dirty = True
            # Player 2 fire
            elif self.game_state == 'player2fire':
                self.shell.update_shell_position("right")
                self.dirty = True  # shell moved, animate it
                shell_value = self.detect_hit_swept("right")
                if shell_value >= 20:
                    self.game_state = 'game_over_2'
                elif shell_value >= 10:
                    print("player2 - Missed")
                    self.key_mode = "angle"
                    self.game_state = 'player1'
            # Game over: the loser gets the first turn in the next round
            elif self.game_state in ('game_over_1', 'game_over_2'):
                if button_b.pressed():
                    loser = "player2" if self.game_state == "game_over_1" else "player1"
                    self.setup(first_player=loser)

# --- Main Entry Point ---
if __name__ == "__main__":
    game = Game(display, led)
    game.run()

