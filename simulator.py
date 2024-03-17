"""
Name: simulator.py
Authors: Tiwari
Date Created: 3/10/24
Date Modified: 3/15/24 SAT
Version: 0.0.1
References:
"""

# Imports
import numpy as np
import random
from slam import Slam
from dynamicTSP import DynamicTSP
from travellingSalesman import TravellingSalesman

# Class
class Simulator:
    def __init__(self, min_length=100, max_length=200, width=50, sensor_range=5.0,noise=1.0):
        self.width = width # y position/axis
        self.sensor_range=sensor_range
        self.noise = noise # we may introduce a noise variable to account for bad measurements that may happen
        self.length = random.randint(min_length, max_length) # x position/axis
        self.grid = [[set() for _ in range(self.length)] for _ in range(self.width)]
        self.robot_pos = [width//2,0]  # Start position, middle side of pipe
        self.debris_types = ['chips', 'tape', 'mag']  # three types of debris: metal chips, tape/residue, magnetic chips
        self.mode = 0  # Start with the first cleaning mode
        self.debris_locations = []
        self.populate_debris(0.1)

    def start_simulation(self):
        slam = Slam(self)
        slam.explore_and_map()
        # path = tsp.find_path()
        # self.clean_pipe(path)
        # Convert set of debris locations to a list of coordinates for TSP
        tsp_locations = [loc for loc, _ in enumerate(self.debris_locations)]
        # Calculate distances between debris locations
        distances = DynamicTSP.calculate_distances(tsp_locations)
        distances2 = DynamicTSP.calculate_distances(tsp_locations)
        dynamicTsp = DynamicTSP(distances)
        tsp = TravellingSalesman(distances2)
        #path,cost=dynamicTsp.dynamic_tsp()
        path,cost=tsp.tsp()


        self.clean_path(path)

    def clean_path(self, path):
        print("Cleaning path:", path)
        for i in path:
            x, y = self.debris_locations[i]
            if self.debris_types[self.mode] in self.grid[x][y]:
                self.grid[x][y].remove(self.debris_types[self.mode])
                print(f"Cleaned {self.debris_types[self.mode]} at {x}, {y}")


    def update_slam(self):
        # update slam
        # TODO: logic here, update pos and debris?
        pass

    def tsp_optimization(self):
        # TODO: finish me
        pass

    def clean_pipe(self, optimized_path):
        pass

    def get_debris(self):
        # TODO: Based on exploration, return a list of debris locations
        return []


    def populate_debris(self, density=0.1):
        # Populate grid with debris, allowing multiple types at each location
        for _ in range(int(self.width * self.length * density)):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
            debris_type = random.choice(self.debris_types)
            self.grid[x][y].add(debris_type)
            self.debris_locations.append((x, y))

    def print_grid(self):
        # Print the grid with debris locations
        for row in self.grid:
            print(' '.join([str(len(cell)) if cell else '.' for cell in row]))

    # returns a positive, random float
    def rand(self):
        return random.random() * 2.0 - 1.0
    

    # # main move function
    # def move(self, dx, dy):    
    #     x = self.robot_pos[0] + dx + (self.rand()*2.0-1.0) * self.noise
    #     y = self.robot_pos[1] + dy + (self.rand()*2.0-1.0) * self.noise

    #     # ensure bounds followed
    #     if 0 <= x < self.width and 0 <= y < self.length:
    #         self.robot_pos = [int(x), int(y)]
    #         return True
    #     return False


    def move(self, dx, dy):
        x, y = self.robot_pos
        x += dx + (self.rand() * self.noise)
        y += dy + (self.rand() * self.noise)
        # Clamp values to ensure bounds
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.length - 1))
        self.robot_pos = [int(x), int(y)]



    # TODO: cleaning mode functions, switch between three cleaning modes
    def switch_mode(self):
        # Switch between cleaning modes
        self.mode = (self.mode + 1) % len(self.debris_types)

    # TODO: cleaning functions, do cleaning if available
    def clean_current_location(self):
        # Clean debris at the robot's current position based on the current mode
        x, y = self.robot_pos
        if self.debris_types[self.mode] in self.grid[x][y]:
            self.grid[x][y].remove(self.debris_types[self.mode])
            print(f"Cleaned {self.debris_types[self.mode]} at {x}, {y}")
