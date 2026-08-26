"""Local smoke test: runs the game logic on the host with stubbed
MicroPython/Pimoroni modules. Not deployed to the Pico."""
import sys, types, random, math

# --- Stub MicroPython/Pimoroni modules ---
class FakePin:
    IN = 0; PULL_UP = 1
    def __init__(self, *a, **k): pass
    def value(self): return 1  # not pressed

machine = types.ModuleType("machine"); machine.Pin = FakePin
utime = types.ModuleType("utime")
utime.sleep = lambda s: None
utime.ticks_ms = lambda: 0
utime.ticks_add = lambda a, b: a + b
utime.ticks_diff = lambda a, b: a - b

class FakeDisplay:
    def __init__(self): self.pens = 0
    def get_bounds(self): return (240, 135)
    def set_backlight(self, v): pass
    def create_pen(self, r, g, b):
        assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255, (r, g, b)
        self.pens += 1; return self.pens
    def set_pen(self, p): pass
    def line(self, *a): pass
    def rectangle(self, *a): pass
    def pixel(self, *a): pass
    def pixel_span(self, *a): pass
    def text(self, *a, **k): pass
    def set_font(self, f): pass
    def update(self): pass

pg = types.ModuleType("picographics")
pg.PicoGraphics = lambda **k: FakeDisplay()
pg.DISPLAY_PICO_DISPLAY = 0; pg.PEN_RGB565 = 0
pim = types.ModuleType("pimoroni")
class FakeLED:
    def __init__(self, *a): pass
    def set_rgb(self, *a): pass
pim.RGBLED = FakeLED

sys.modules.update(machine=machine, utime=utime, picographics=pg, pimoroni=pim)

import main  # noqa: E402
game = main.Game(main.display, main.led)

# --- Test 1: swept collision cannot tunnel through a tank ---
game.terrain.terrain_y_positions = [130] * 240
game.tank2.set_position((200, 130))
r = game.tank2.get_rect()
game.shell.previous_position = (r[0] - 10, (r[1] + r[3]) / 2)
game.shell.current_position = (r[2] + 10, (r[1] + r[3]) / 2)
assert game.detect_hit_swept("left") == 20, "swept detection missed the tank!"
print("PASS: swept detection catches tunneling shell")

# --- Test 2: point detection codes ---
game.shell.current_position = (300, 50)
assert game.detect_hit("left") == 10
game.shell.current_position = (120, -50)
assert game.detect_hit("left") == 1
game.shell.current_position = (120, 200)
assert game.detect_hit("left") == 11
game.shell.current_position = (120, 132)
assert game.detect_hit("left") == 11
print("PASS: detect_hit codes correct (bottom edge now ground=11)")

# --- Test 3: full game simulation, random shots until game over ---
random.seed(42)
for trial in range(200):
    game.setup()
    for turn in range(50000):
        state = game.game_state
        if state in ("player1", "player2"):
            side = "left" if state == "player1" else "right"
            tank = game.tank1 if side == "left" else game.tank2
            tank.set_gun_angle(random.choice(range(0, 86, 5)))
            tank.set_gun_power(random.choice(range(10, 101, 5)))
            gp = tank.calc_gun_positions()
            sp = (gp[3][0], gp[3][1] + 2)
            game.shell.set_start_position(sp)
            game.shell.set_angle(math.radians(tank.get_gun_angle()))
            game.shell.set_power(tank.get_gun_power() / 40)
            game.shell.set_time(0)
            game.game_state = state + "fire"
        elif state in ("player1fire", "player2fire"):
            side = "left" if state == "player1fire" else "right"
            game.shell.update_shell_position(side)
            v = game.detect_hit_swept(side)
            if v >= 20:
                game.game_state = "game_over_1" if side == "left" else "game_over_2"
            elif v >= 10:
                game.game_state = "player2" if side == "left" else "player1"
        else:
            break
    else:
        raise AssertionError("game never ended in trial %d" % trial)
print("PASS: 200 simulated games all reached game over")

# --- Test 4: Button edge/repeat logic ---
t = [0]
utime.ticks_ms = lambda: t[0]
btn = main.Button(12, repeat=(250, 100))
class P:
    v = 1
    def value(self): return self.v
btn.pin = P()
btn.pin.v = 0
assert btn.pressed() is True, "edge should fire"
assert btn.pressed() is False, "held, before repeat delay"
t[0] = 260
assert btn.pressed() is True, "first repeat"
t[0] = 300
assert btn.pressed() is False, "before next repeat"
t[0] = 370
assert btn.pressed() is True, "second repeat"
btn.pin.v = 1
assert btn.pressed() is False, "released"
btn.pin.v = 0
assert btn.pressed() is True, "new edge"
print("PASS: Button edge-trigger + hold-repeat works")

print("All smoke tests passed.")
