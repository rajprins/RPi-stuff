import math
import random

# Creates the terrain for the tanks to go on.
# Also positions the tanks - which can be retrieved using get_tank_position method

# How big a chunk to split up x axis
TERRAIN_CHUNK_SIZE = 20

# Max that terrain can go up or down within chunk size
TERRAIN_MAX_CHG = 20

# Max height of ground
TERRAIN_MIN_Y = 50

# Size of terrain for tank
TERRAIN_TANK_SIZE = 20

class Terrain:
    
    def __init__ (self, display, ground_color):
        self.display = display
        self.ground_color = ground_color
        width, height = display.get_bounds()
        self.screen_size = (width, height)
        self.setup()
        
    def setup(self):
        
        # Create an array of terrain y values - gravity means that all blocks below are solid (no caves)
        # Initially all set to 0
        width = self.screen_size[0]
        height = self.screen_size[1]
        
        self.terrain_y_positions = [0] * width
        
        # Setup terrainscape (these positions represent left side of platform)
        # Choose a random position (temp values - to be stored in tank object)
        # The complete x,y co-ordinates will be saved in a tuple in left_tank_rect and right_tank_rect
        # includes a DMZ of 40 pixels
        left_tank_x_position = random.randint (10,int(width/2)-30)
        right_tank_x_position = random.randint (int(width/2)+30, width-40)
        
        self.tank1_position = (left_tank_x_position,0)
        self.tank2_position = (right_tank_x_position,0)
        
        # Sub divide screen into chunks for the terrainscape
        current_terrain_x = 0
        next_terrain_x = 0 + TERRAIN_CHUNK_SIZE
        # start y position at least 50 from top 20 from bottom
        current_terrain_y = random.randint (50,self.screen_size[1]-20)
        self.terrain_y_positions[current_terrain_x] = current_terrain_y
        
        while (current_terrain_x < self.screen_size[0]):
            # If where tank is then we create a flat area for tank to sit on
            if (current_terrain_x == left_tank_x_position):
                # handle tank platform
                self.tank1_position = (current_terrain_x, int(current_terrain_y))
                # Add another 60 pixels further along at same y position (level ground for tank to sit on)
                for i in range (0, TERRAIN_TANK_SIZE):
                    self.terrain_y_positions[current_terrain_x] = int(current_terrain_y)
                    current_terrain_x += 1
                continue
            elif (current_terrain_x == right_tank_x_position):
                # handle tank platform
                self.tank2_position = (current_terrain_x, int(current_terrain_y))
                # Add another 60 pixels further along at same y position (level ground for tank to sit on)
                for i in range (0, TERRAIN_TANK_SIZE):
                    self.terrain_y_positions[current_terrain_x] = int(current_terrain_y)
                    current_terrain_x += 1
                continue
            
            # Checks to see if next position will be where the tanks are
            if (current_terrain_x < left_tank_x_position and current_terrain_x + TERRAIN_CHUNK_SIZE >= left_tank_x_position):
                # set x position to tank position
                next_terrain_x = left_tank_x_position
            elif (current_terrain_x < right_tank_x_position and current_terrain_x + TERRAIN_CHUNK_SIZE >= right_tank_x_position):
                # set x position to tank position
                next_terrain_x = right_tank_x_position
            elif (current_terrain_x + TERRAIN_CHUNK_SIZE > self.screen_size[0]):
                next_terrain_x = self.screen_size[0] 
            else:
                next_terrain_x = current_terrain_x + TERRAIN_CHUNK_SIZE
            # Set the y height
            next_terrain_y = current_terrain_y + random.randint(0-TERRAIN_MAX_CHG,TERRAIN_MAX_CHG)
            # check not too high or too lower (note the reverse logic as high y is bottom of screen)
            if (next_terrain_y > self.screen_size[1]):   # Bottom of screen
                next_terrain_y = self.screen_size[1]
            if (next_terrain_y < TERRAIN_MIN_Y):
                next_terrain_y = TERRAIN_MIN_Y
            # Add to list
            # Work through until current_terrain_x = next_terrain_x
            # delta is how much the y value changes per increment
            # Check not flat first
            if (next_terrain_y == current_terrain_y or next_terrain_x == current_terrain_x):
                y_delta = 0
            else:
                y_delta = (next_terrain_y - current_terrain_y) / (next_terrain_x - current_terrain_x)
            for i in range (current_terrain_x, next_terrain_x):
                current_terrain_y += y_delta
                self.terrain_y_positions[current_terrain_x] = int(current_terrain_y)
                current_terrain_x += 1
            

    def get_tank1_position(self):
        return self.tank1_position
        
    def get_tank2_position(self):
        return self.tank2_position
        
    # checks if a x,y position is ground or not
    def is_ground(self, x, y):
        if (y >= self.terrain_y_positions[x]):
            return True
        return False

    def draw (self):
        self.display.set_pen(self.ground_color)
        current_terrain_x = 0
        for this_pos in self.terrain_y_positions:
            for this_y in range (self.terrain_y_positions[current_terrain_x], self.screen_size[1]):
                self.display.pixel(current_terrain_x, int(this_y))
            current_terrain_x += 1
