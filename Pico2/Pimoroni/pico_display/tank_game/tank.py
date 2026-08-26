import math
import random

# Tank colors are supplied by the caller (see main.py) via the constructor,
# so no color constants are needed here.

# Gun barrel dimensions (in pixels)
GUN_LENGTH = 10
GUN_DIAMETER = 2


class Tank:
    def __init__(self, display, left_right, tank_color):
        self.display = display
        self.left_right = left_right
        self.tank_color = tank_color
        self.position = (0, 0)

        # Angle that the gun is pointing (degrees relative to horizontal)
        # We randomize the angle for more challenge...
        self.gun_angle = random.choice(range(0, 61, 5))

        # Amount of power to fire with
        # We randomize this too for more challenge...
        self.gun_power = random.choice(range(25, 51, 5))

    def reset(self):
        self.gun_angle = random.choice(range(0, 61, 5))
        self.gun_power = random.choice(range(25, 51, 5))

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    # Returns a bounding rectangle for collision detection
    # returns tuple x1, y1, x2, y2
    def get_rect(self):
        return (
            self.position[0] + 4,
            self.position[1] - 14,
            self.position[0] + 28,
            self.position[1],
        )

    def set_gun_angle(self, angle):
        self.gun_angle = angle

    def change_gun_angle(self, amount):
        self.gun_angle += amount
        if self.gun_angle > 85:
            self.gun_angle = 85
        if self.gun_angle < 0:
            self.gun_angle = 0

    def get_gun_angle(self):
        return self.gun_angle

    def set_gun_power(self, power):
        self.gun_power = power

    def change_gun_power(self, amount):
        self.gun_power += amount
        if self.gun_power > 100:
            self.gun_power = 100
        if self.gun_power < 10:
            self.gun_power = 10

    def get_gun_power(self):
        return self.gun_power

    # Draws tank (including gun - which depends upon direction and aim)
    # self.left_right can be "left" or "right" to depict which position the tank is in
    # tank_start_pos requires x, y co-ordinates as a tuple
    # angle is relative to horizontal - in degrees
    def draw(self):
        self.display.set_pen(self.tank_color)

        # Tracks
        self.display.pixel_span(self.position[0] + 6, self.position[1] - 10, 20)
        self.display.pixel_span(self.position[0] + 5, self.position[1] - 9, 22)
        self.display.pixel_span(self.position[0] + 4, self.position[1] - 8, 24)
        self.display.pixel_span(self.position[0] + 3, self.position[1] - 7, 26)
        self.display.pixel_span(self.position[0] + 2, self.position[1] - 6, 28)
        self.display.pixel_span(self.position[0] + 1, self.position[1] - 5, 30)
        self.display.pixel_span(self.position[0] + 2, self.position[1] - 4, 28)
        self.display.pixel_span(self.position[0] + 3, self.position[1] - 3, 26)
        self.display.pixel_span(self.position[0] + 4, self.position[1] - 2, 24)
        self.display.pixel_span(self.position[0] + 5, self.position[1] - 1, 22)
        self.display.pixel_span(self.position[0] + 6, self.position[1], 20)

        # Hull
        self.display.rectangle(self.position[0] + 7, self.position[1] - 13, 18, 3)

        self.display.pixel_span(self.position[0] + 8, self.position[1] - 14, 16)
        self.display.pixel_span(self.position[0] + 6, self.position[1] - 15, 20)
        self.display.pixel_span(self.position[0] + 8, self.position[1] - 16, 16)

        # Gun position involves more complex calculations so in a separate function
        self.draw_gun(self.calc_gun_positions())

    # Draw gun on tank - a single native thick line from the barrel base
    # to the muzzle. PicoGraphics line() accepts a thickness parameter,
    # which replaces the old per-pixel Python loop (one native call
    # instead of ~20 pixel() calls per tank per frame).
    def draw_gun(self, gun_positions):
        start_x, start_y = gun_positions[1]
        end_x, end_y = gun_positions[2]
        self.display.line(
            int(start_x), int(start_y),
            int(end_x), int(end_y),
            GUN_DIAMETER,
        )

    # Calculate the polygon positions for the gun barrel
    # This calculates a polygon based on the pygame zero method
    # For the Pico version use point 0 and 1 for drawing line for barrel
    def calc_gun_positions(self):
        (xpos, ypos) = self.position
        # Set the start of the gun (top of barrel at point it joins the tank)
        if self.left_right == "right":
            gun_start_pos_top = (xpos + 6, ypos - 15)
        else:
            gun_start_pos_top = (xpos + 26, ypos - 15)

        # Convert angle to radians (for right subtract from 180 deg first)
        relative_angle = self.gun_angle
        if self.left_right == "right":
            relative_angle = 180 - self.gun_angle
        angle_rads = relative_angle * (math.pi / 180)
        # Create vector based on the direction of the barrel
        # Y direction *-1 (due to reverse y of screen)
        gun_vector = (math.cos(angle_rads), math.sin(angle_rads) * -1)

        # Determine position bottom of barrel
        # Create temporary vector 90deg to existing vector
        if self.left_right == "right":
            temp_angle_rads = math.radians(relative_angle - 90)
        else:
            temp_angle_rads = math.radians(relative_angle + 90)
        temp_vector = (math.cos(temp_angle_rads), math.sin(temp_angle_rads) * -1)

        gun_start_pos_bottom = (
            gun_start_pos_top[0] + temp_vector[0] * GUN_DIAMETER,
            gun_start_pos_top[1] + temp_vector[1] * GUN_DIAMETER,
        )

        # Calculate barrel positions based on vector from start position
        gun_positions = [
            gun_start_pos_bottom,
            gun_start_pos_top,
            (
                gun_start_pos_top[0] + gun_vector[0] * GUN_LENGTH,
                gun_start_pos_top[1] + gun_vector[1] * GUN_LENGTH,
            ),
            (
                gun_start_pos_bottom[0] + gun_vector[0] * GUN_LENGTH,
                gun_start_pos_bottom[1] + gun_vector[1] * GUN_LENGTH,
            ),
        ]

        return gun_positions
