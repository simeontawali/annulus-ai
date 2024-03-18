"""
Simultaneous Localization and Mapping (SLAM): algorithm for initial exploration phase. 
autonomously explore and map the interior of pipe. 
If implementation is too complicated, it could be done with breadth or 
depth first search and just explore every grid point. 
This implementation seeks to map out the entire grid without visiting every square. 
SLAM builds a map and localizes the vehicle in that map at the same time.

Authors: Tiwari, Yuen
Date Created: 3/11/24
Date Modified: 3/17/24 TSA, YN
Version: 0.0.1
References:
https://www.geeksforgeeks.org/simultaneous-localization-and-mapping/
https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/

"""
import random
import numpy as np
import math

class Slam:
    def __init__(self,simulator):
        self.simulator = simulator
        self.grid = np.array(simulator.grid)  # Make a copy
        self.visited = set()  # Keep track of visited locations
        self.moves = 0

    def explore_and_map(self):
        # Use a queue for BFS exploration
        queue = [tuple(self.simulator.robot_pos)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 possible movements

        while queue:
            current_pos = self.simulator.robot_pos
            candidate_pos = queue.pop(0)
            cx,cy = current_pos
            nx,ny=candidate_pos
            if candidate_pos not in self.visited:
                self.visited.add(candidate_pos)
            dx,dy = nx-cx,ny-cy
            self.simulator.move(dx,dy)
            self.moves += (abs(dx)+abs(dy))
            self.detect_debris(nx, ny)
            #self.simulator.clean_grid(cx,cy)
            # Explore neighboring cells
            for dx, dy in directions:
                new_pos = (nx + dx, ny + dy)
                new_x,new_y = new_pos
                # new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.simulator.width) and (0 <= new_y < self.simulator.length) and ((new_x, new_y) not in self.visited):
                    queue.append(new_pos)
                    if new_pos not in self.visited:
                        self.visited.add(new_pos)
                    # self.visited.add(new_pos)
                    # self.simulator.move(dx, dy)
                    # self.detect_debris(nx,ny)
                    # self.moves += abs(dx)+abs(dy)
                    # self.simulator.clean_grid(nx,ny)
        cx,cy = self.simulator.robot_pos
        self.simulator.move(-cx,-cy) # return home
        self.moves += (cx+cy)    
                    

    def detect_debris(self, x, y):
        # Simulate sensor range and accuracy. For simplicity, assume 100% accuracy within sensor range.
       # sensor_range = self.simulator.sensor_range
       # for i in range(max(0, x - sensor_range), min(self.simulator.width, x + sensor_range + 1)):
        #    for j in range(max(0, y - sensor_range), min(self.simulator.length, y + sensor_range + 1)):
             #   if self.simulator.grid[i][j]:  # If theres debris
                    # Update the local class grid with detected debris
              #      if((x,y) not in self.simulator.debris_locations):
               #         self.simulator.debris_locations.append((x, y))
                #    self.grid[i][j] = self.simulator.grid[i][j].copy()
        if self.simulator.grid[x][y]:  # If there's debris
            if (x, y) not in self.simulator.debris_locations:
                self.simulator.debris_locations.append((x, y))
                self.simulator.clean_grid(x,y)


    def print_mapped_area(self):
        # Print the mapped area for visualization
        for row in self.grid:
            print(' '.join(['X' if cell else '.' for cell in row]))

                    

    # # IGNORE ME:
    # def robot_vision(self, robot_pos, length, width):
    #     # lets start by saying robot can see 4 ahead and 2 adjacent grids, we will define acuracy levels
    #     # for these grids and say that it knows with certianty what is up close and can predict what is far
    #     visible_cells = []
    #     # Direct line of sight with 100% accuracy up to 2 grids forward
    #     for i in range(1, 3):
    #         if self.robot_pos[1] + i < length:
    #             visible_cells.append((robot_pos[0], robot_pos[1] + i))
        
    #     # 4 grids forward with 50% accuracy
    #     for i in range(3, 5):
    #         if robot_pos[1] + i < length and random.random() < 0.5:
    #             visible_cells.append((robot_pos[0], robot_pos[1] + i))
        
    #     # Adjacent grid in line of sight 2 grids forward with 75% accuracy
    #     if robot_pos[1] + 2 < length and random.random() < 0.75:
    #         if robot_pos[0] > 0:  # Left side
    #             visible_cells.append((robot_pos[0] - 1, robot_pos[1] + 2))
    #         if robot_pos[0] < width - 1:  # Right side
    #             visible_cells.append((robot_pos[0] + 1, robot_pos[1] + 2))

    #     return visible_cells

    # def sense_debris(self, robot_pos, sensor_range, debris_locations, noise):
    #     measurements = []
    #     for index, (dx, dy) in enumerate(debris_locations):
    #         distance_x = dx - robot_pos[0]
    #         distance_y = dy - robot_pos[1]
    #         distance_x += (random.random() * 2.0 - 1.0) * noise
    #         distance_y += (random.random() * 2.0 - 1.0) * noise

    #         if abs(distance_x) < sensor_range and abs(distance_y) < sensor_range:
    #             measurements.append([index, distance_x, distance_y])
    #     return measurements
