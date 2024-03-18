"""
Name: simulator.py
Authors: Tiwari
Date Created: 3/10/24
Date Modified: 3/17/24 TSA, YN
Version: 0.0.1
References:
"""

# Imports
import sys
import numpy as np
import random
from slam import Slam
from dynamicTSP import dynamic_tsp
from halfDynamicSalesman import HalfDynamicTSP
from travellingSalesman import TravellingSalesman
import os, time
from timeit import default_timer

# Class
class Simulator:
    def __init__(self, min_length=15, max_length=15, width=15,noise=0):
        self.width = width # y position/axis
        self.noise = noise # we may introduce a noise variable to account for bad measurements that may happen
        self.length = random.randint(min_length, max_length) # x position/axis
        self.grid = [[set() for _ in range(self.length)] for _ in range(self.width)]
        self.robot_pos = [0,0]  # Start position, middle side of pipe
        self.debris_types = ['Chips','Tape']  # three types of debris: metal chips, tape/residue, magnetic chips
        self.mode = 0  # Start with the first cleaning mode
        self.optimized_moves = 0
        self.debris_locations = []
        self.populate_debris(1)

    def start_simulation(self):
        slam = Slam(self)
        print("Initial Grid")
        self.print_grid()

        start = default_timer()
        slam.explore_and_map()
        print(f"Slam took {default_timer() - start} seconds")

        print(f"\nSlam takes: {slam.moves} moves\n")
        print("New Grid after Slam:")
        self.print_grid()
        # slam should update the array debris locations
        print("\nRobot returns home and changes cleaning mode\n")
        self.switch_mode()
        #self.clean_path(path)
        #print(self.debris_locations)
        start = default_timer()
        typeDistances = Simulator.create_distances(self.debris_locations)
        dynaTSPpath = HalfDynamicTSP.dynamic_tsp(typeDistances)
        path,cost = dynaTSPpath
        print(f"HalfDynaTSP took {default_timer() - start} seconds")

        print(f"\nDynamic TSP gives an optimized path of: {dynaTSPpath}\n")
        self.clean_path(path)
        print(f"\nDynamic TSP took {cost} moves\n")
        print("Final Grid:")
        self.print_grid()

        #dynaTSPpath = HalfDynamicTSP.dynamic_tsp(typeDistances)
        # newList = []
        # for i in range(len(typeDistances)):
        #     newList.append(i)
        # print(newList)
        # shallow_dis = typeDistances
        # print(dynamic_tsp(newList, 0, 0, [0]*len(typeDistances), shallow_dis))
        #print(dynaTSPpath)

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
                print(f"Cleaned {self.debris_types[self.mode]} at {next_x}, {next_y}", end="\r")


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
    
    def move(self, dx, dy):
        x, y = self.robot_pos
        x += dx + (self.rand() * self.noise)
        y += dy + (self.rand() * self.noise)
        # Clamp values to ensure bounds
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.length - 1))
        self.robot_pos = [int(x), int(y)]
        print(f"Pos: {x}, {y}", end="\r")

    def switch_mode(self):
        # Switch between cleaning modes
        self.mode = (self.mode + 1) % len(self.debris_types)

    def clean_grid(self,x,y):
        if self.debris_types[self.mode] in self.grid[x][y]:
            self.grid[x][y].remove(self.debris_types[self.mode])
            print(f"Cleaned {self.debris_types[self.mode]} at {x}, {y}", end="\r")

    # cleaning functions, do cleaning if available
    def clean_current_location(self):
        # Clean debris at the robot's current position based on the current mode
        x, y = self.robot_pos
        if self.debris_types[self.mode] in self.grid[x][y]:
            self.grid[x][y].remove(self.debris_types[self.mode])
            print(f"Cleaned {self.debris_types[self.mode]} at {x}, {y}", end="\r")
        
    def updatable_grid(self):
        # clear
        os.system('cls' if os.name == 'nt' else 'clear')

        # iter over each row and column to print the grid
        for i, row in enumerate(self.grid):
            row_str = ''
            for j, cell in enumerate(row):
                if [i, j] == self.robot_pos:
                    row_str += 'X  '  # position with 'X'
                else:
                    row_str += (str(len(cell)) + ' ') if cell else '.  '  # '.' for empty
            print(row_str.rstrip())  # each row of the grid


sim = Simulator()
sim.start_simulation()