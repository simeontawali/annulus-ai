"""
Simultaneous Localization and Mapping (SLAM): algorithm for initial exploration phase. 
autonomously explore and map the interior of pipe. 
If implementation is too complicated, it could be done with breadth or 
depth first search and just explore every grid point. 
This implementation seeks to map out the entire grid without visiting every square. 
SLAM builds a map and localizes the vehicle in that map at the same time.

Authors: Tiwari, Yuen
Date Created: 3/11/24
Date Modified: 3/15/24 SAT
Version: 0.0.1
References:
https://www.geeksforgeeks.org/simultaneous-localization-and-mapping/

"""
import random

class Slam:
    def __init__(self, grid, start_pos):
        self.grid = grid
        self.robot_pos = start_pos
        self.visited = set()
        self.to_visit = [start_pos]

    def explore(self):
        while self.to_visit:
            current_pos = self.to_visit.pop(0)
            if current_pos in self.visited:
                continue
            self.visited.add(current_pos)
            for direction in [(0,1), (1,0), (0,-1), (-1,0)]: # Explore in all four directions
                next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if 0 <= next_pos[0] < self.grid.shape[0] and 0 <= next_pos[1] < self.grid.shape[1]:
                    self.to_visit.append(next_pos)
                    # Simulate sensor data collection here if needed
        # Update the grid or robot's knowledge base with explored data
                    


    def robot_vision(self, robot_pos, length, width):
        # lets start by saying robot can see 4 ahead and 2 adjacent grids, we will define acuracy levels
        # for these grids and say that it knows with certianty what is up close and can predict what is far
        visible_cells = []
        # Direct line of sight with 100% accuracy up to 2 grids forward
        for i in range(1, 3):
            if self.robot_pos[1] + i < length:
                visible_cells.append((robot_pos[0], robot_pos[1] + i))
        
        # 4 grids forward with 50% accuracy
        for i in range(3, 5):
            if robot_pos[1] + i < length and random.random() < 0.5:
                visible_cells.append((robot_pos[0], robot_pos[1] + i))
        
        # Adjacent grid in line of sight 2 grids forward with 75% accuracy
        if robot_pos[1] + 2 < length and random.random() < 0.75:
            if robot_pos[0] > 0:  # Left side
                visible_cells.append((robot_pos[0] - 1, robot_pos[1] + 2))
            if robot_pos[0] < width - 1:  # Right side
                visible_cells.append((robot_pos[0] + 1, robot_pos[1] + 2))

        return visible_cells

    def sense_debris(self, robot_pos, sensor_range, debris_locations, noise):
        measurements = []
        for index, (dx, dy) in enumerate(debris_locations):
            distance_x = dx - robot_pos[0]
            distance_y = dy - robot_pos[1]
            distance_x += (random.random() * 2.0 - 1.0) * noise
            distance_y += (random.random() * 2.0 - 1.0) * noise

            if abs(distance_x) < sensor_range and abs(distance_y) < sensor_range:
                measurements.append([index, distance_x, distance_y])
        return measurements
