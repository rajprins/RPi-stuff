import random

# --- Terrain Constants ---
TERRAIN_CHUNK_SIZE = 20
TERRAIN_MAX_CHG = 20
TERRAIN_MIN_Y = 50
TERRAIN_TANK_SIZE = 20

class Terrain:
    def __init__(self, display, ground_color):
        self.display = display
        self.ground_color = ground_color
        self.width, self.height = display.get_bounds()
        self.terrain_y_positions = [0] * self.width
        self.tank1_position = (0, 0)
        self.tank2_position = (0, 0)
        self.setup()

    def setup(self):
        width, height = self.width, self.height
        terrain = self.terrain_y_positions

        left_tank_x = random.randint(10, width // 2 - 30)
        right_tank_x = random.randint(width // 2 + 30, width - 40)
        self.tank1_position = (left_tank_x, 0)
        self.tank2_position = (right_tank_x, 0)

        current_x = 0
        current_y = random.randint(50, height - 20)
        terrain[current_x] = current_y

        while current_x < width:
            # Flat platform for tanks
            if current_x == left_tank_x or current_x == right_tank_x:
                if current_x == left_tank_x:
                    self.tank1_position = (current_x, int(current_y))
                else:
                    self.tank2_position = (current_x, int(current_y))
                for _ in range(TERRAIN_TANK_SIZE):
                    if current_x >= width:
                        break
                    terrain[current_x] = int(current_y)
                    current_x += 1
                continue

            # Find next chunk boundary
            next_x = min(current_x + TERRAIN_CHUNK_SIZE, width)
            # Snap to tank platform if needed
            if current_x < left_tank_x < next_x:
                next_x = left_tank_x
            elif current_x < right_tank_x < next_x:
                next_x = right_tank_x

            # Next y value
            next_y = current_y + random.randint(-TERRAIN_MAX_CHG, TERRAIN_MAX_CHG)
            next_y = max(TERRAIN_MIN_Y, min(next_y, height))

            # Linear interpolation for smooth slope
            steps = max(1, next_x - current_x)
            y_delta = (next_y - current_y) / steps
            for _ in range(steps):
                if current_x >= width:
                    break
                current_y += y_delta
                terrain[current_x] = int(current_y)
                current_x += 1

    def get_tank1_position(self):
        return self.tank1_position

    def get_tank2_position(self):
        return self.tank2_position

    def is_ground(self, x, y):
        if 0 <= x < self.width:
            return y >= self.terrain_y_positions[x]
        return False

    def draw(self):
        self.display.set_pen(self.ground_color)
        # Use vertical lines for each terrain column for better performance
        for x, ground_y in enumerate(self.terrain_y_positions):
            self.display.line(x, ground_y, x, self.height - 1)

