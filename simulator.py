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
    def __init__(self, min_length=100, max_length=200, width=50, sensor_range=5,noise=1.0):
        self.width = width # y position/axis
        self.sensor_range=sensor_range
        self.noise = noise # we may introduce a noise variable to account for bad measurements that may happen
        self.length = random.randint(min_length, max_length) # x position/axis
        self.grid = np.zeros((self.width, self.length))
        self.robot_pos = (0, 0)  # Start position
        self.debris_types = [1, 2, 3]  # three types of debris: metal chips, tape/residue, magnetic chips
        # FIXME: should debris types be "chips","tape","mag"
        self.mode = 1  # Start with the first cleaning mode

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
    

    # alternate move function assuming move is not accurate
    # should we use this??
    def move(self, dx, dy):    
        x = self.robot_pos[0] + dx + self.rand() * self.noise
        y = self.robot_pos[1] + dy + self.rand() * self.noise

        if x < 0.0 or x > self.length or y < 0.0 or y > self.width:
            return False
        else:
            self.robot_pos[0] = x
            self.robot_pos[1] = y
            return True


    # perfect move function??
    def move_robot(self, direction):
        if direction == 'up' and self.robot_pos[0] > 0:
            self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1])
        elif direction == 'down' and self.robot_pos[0] < self.width - 1:
            self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1])
        elif direction == 'right' and self.robot_pos[1] < self.length - 1:
            self.robot_pos = (self.robot_pos[0], self.robot_pos[1] + 1)
        elif direction == 'left' and self.robot_pos[1] < self.length - 1:
            self.robot_pos = (self.robot_pos[0], self.robot_pos[1] - 1)


    def robot_vision(self):
        # lets start by saying robot can see 4 ahead and 2 adjacent grids, we will define acuracy levels
        # for these grids and say that it knows with certianty what is up close and can predict what is far
        visible_cells = []
        # Direct line of sight with 100% accuracy up to 2 grids forward
        for i in range(1, 3):
            if self.robot_pos[1] + i < self.length:
                visible_cells.append((self.robot_pos[0], self.robot_pos[1] + i))
        
        # 4 grids forward with 50% accuracy
        for i in range(3, 5):
            if self.robot_pos[1] + i < self.length and random.random() < 0.5:
                visible_cells.append((self.robot_pos[0], self.robot_pos[1] + i))
        
        # Adjacent grid in line of sight 2 grids forward with 75% accuracy
        if self.robot_pos[1] + 2 < self.length and random.random() < 0.75:
            if self.robot_pos[0] > 0:  # Left side
                visible_cells.append((self.robot_pos[0] - 1, self.robot_pos[1] + 2))
            if self.robot_pos[0] < self.width - 1:  # Right side
                visible_cells.append((self.robot_pos[0] + 1, self.robot_pos[1] + 2))

        return visible_cells

    # TODO: cleaning mode functions
    # TODO: cleaning functions
    