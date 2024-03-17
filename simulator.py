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
        self.grid = np.zeros((self.width, self.length))
        self.robot_pos = [width//2,0]  # Start position, middle side of pipe
        self.debris_types = [1, 2, 3]  # three types of debris: metal chips, tape/residue, magnetic chips
        self.debris_locations = []
        # FIXME: should debris types be "chips","tape","mag"
        self.mode = 0  # Start with the first cleaning mode

    def start_simulation(self):
        slam = Slam()
        tsp = TravellingSalesman()
        dynamicTsp = DynamicTSP()
        self.populate_debris(0.1)

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
        for _ in range(int(self.width * self.length * density)):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
            self.grid[x][y] = random.choice(self.debris_types)
            # TODO: allow one grid location to store multiple debris types

    def print_grid(self):
        print(self.grid.T)  # Transpose and visualization

    # returns a positive, random float
    def rand(self):
        return random.random() * 2.0 - 1.0
    

    # main move function
    def move(self, dx, dy):    
        x = self.robot_pos[0] + dx + (self.rand()*2.0-1.0) * self.noise
        y = self.robot_pos[1] + dy + (self.rand()*2.0-1.0) * self.noise

        # ensure bounds followed
        if 0 <= x < self.width and 0 <= y < self.length:
            self.robot_pos = [int(x), int(y)]
            return True
        return False


    # other move function?? may not work for left/right
    def move_robot(self, direction):
        if direction == 'up' and self.robot_pos[0] > 0:
            self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1])
        elif direction == 'down' and self.robot_pos[0] < self.width - 1:
            self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1])
        elif direction == 'right' and self.robot_pos[1] < self.length - 1:
            self.robot_pos = (self.robot_pos[0], self.robot_pos[1] + 1)
        elif direction == 'left' and self.robot_pos[1] < self.length - 1:
            self.robot_pos = (self.robot_pos[0], self.robot_pos[1] - 1)



    # TODO: cleaning mode functions, switch between three cleaning modes
    # TODO: cleaning functions, do cleaning if available
    