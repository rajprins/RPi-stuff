import math


class Shell:
    GRAVITY = 0.008
    DISTANCE_SCALE = 1.5
    TIME_STEP = 4

    def __init__(self, display, shell_color):
        self.display = display
        self.shell_color = shell_color
        self.reset()

    def reset(self):
        self.start_position = (0, 0)
        self.current_position = (0, 0)
        self.power = 1
        self.angle = 0
        self.time = 0

    def set_start_position(self, position):
        self.start_position = position
        self.current_position = position

    def get_start_position(self):
        return self.start_position

    def set_current_position(self, position):
        self.current_position = position

    def get_current_position(self):
        return self.current_position

    def set_angle(self, angle):
        self.angle = angle

    def set_power(self, power):
        self.power = power

    def set_time(self, time):
        self.time = time

    def draw(self):
        x, y = self.current_position
        self.display.set_pen(self.shell_color)
        self.display.rectangle(int(x), int(y), 2, 2)

    def update_shell_position(self, left_right):
        vx, vy = self._calculate_initial_velocity(left_right)
        t = self.time
        x0, y0 = self.start_position

        shell_x = x0 + vx * t * self.DISTANCE_SCALE
        shell_y = y0 - ((vy * t) - (0.5 * self.GRAVITY * t * t))

        self.current_position = (shell_x, shell_y)
        self.time += self.TIME_STEP

    def _calculate_initial_velocity(self, left_right):
        if left_right == "left":
            angle = self.angle
        else:
            angle = math.pi - self.angle
        vx = self.power * math.cos(angle)
        vy = self.power * math.sin(self.angle)
        return vx, vy
