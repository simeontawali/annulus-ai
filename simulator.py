"""
Name: simulator.py
Authors: Tiwari
Date Created: 3/10/24
Date Modified: 3/17/24 SAT
Version: 0.0.1
References:
"""

# Imports
import sys
import numpy as np
import random
from slam import Slam
from dynamicTSP import DynamicTSP
from travellingSalesman import TravellingSalesman

# Class
class Simulator:
    def __init__(self, min_length=5, max_length=5, width=5, sensor_range=0,noise=0):
        self.width = width # y position/axis
        self.sensor_range=sensor_range
        self.noise = noise # we may introduce a noise variable to account for bad measurements that may happen
        self.length = random.randint(min_length, max_length) # x position/axis
        self.grid = [[set() for _ in range(self.length)] for _ in range(self.width)]
        self.robot_pos = [0,0]  # Start position, middle side of pipe
        self.debris_types = ['C','T','M']  # three types of debris: metal chips, tape/residue, magnetic chips
        self.mode = 0  # Start with the first cleaning mode
        self.optimized_moves = 0
        self.debris_locations = set()
        self.populate_debris(1)

    def start_simulation(self):
        slam = Slam(self)
        self.print_grid()
        slam.explore_and_map()
        print(slam.moves)
        self.print_grid()

        # slam should update the array debris locations

        # Calculate distances between debris locations
        

        # Call DynaTSP to calculate optimal pat and it's total move cost



        self.mode = 1
        #self.clean_path(path)
        #print(self.debris_locations)
        print(Simulator.create_distances(self.debris_locations))
        self.mode = 2
        #self.clean_path(path)


    def create_distances(debris_locs):
        all_distances = []
        for i in range(len(debris_locs)):
            node_distances = []
            for j in range(len(debris_locs)):
                if(debris_locs[i] == debris_locs[j]):
                    node_distances.append(sys.maxsize)
                else:
                    moves = abs(debris_locs[j][0] - debris_locs[i][0]) + abs(debris_locs[j][1] - debris_locs[i][1])
                    node_distances.append(moves)
            all_distances.append(node_distances)

        return all_distances

    def clean_path(self, path):
        print("Cleaning path:", path)
        for i in path:
            current_x, current_y = self.robot_pos
            next_x, next_y = self.debris_locations[i]
            self.move(next_x-current_x,next_y-current_y)
            self.optimized_moves += (abs(next_x-current_x)+abs(next_y-current_y))
            if self.debris_types[self.mode] in self.grid[next_x][next_y]:
                self.grid[next_x][next_y].remove(self.debris_types[self.mode])
                print(f"Cleaned {self.debris_types[self.mode]} at {next_x}, {next_y}")


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
            # self.debris_locations.append((x, y))

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

    def clean_grid(self,x,y):
        if self.debris_types[self.mode] in self.grid[x][y]:
            self.grid[x][y].remove(self.debris_types[self.mode])
            print(f"Cleaned {self.debris_types[self.mode]} at {x}, {y}")

    # TODO: cleaning functions, do cleaning if available
    def clean_current_location(self):
        # Clean debris at the robot's current position based on the current mode
        x, y = self.robot_pos
        if self.debris_types[self.mode] in self.grid[x][y]:
            self.grid[x][y].remove(self.debris_types[self.mode])
            print(f"Cleaned {self.debris_types[self.mode]} at {x}, {y}")


sim = Simulator()
sim.start_simulation()