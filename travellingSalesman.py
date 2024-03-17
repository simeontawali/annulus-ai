"""
TSP-Based Path Optimization: Given the locations of different types of debris 
identified during the exploration phase, formulate this as a TSP, 
where each debris location is a city that the robot must visit. 
The objective is to find the shortest possible path that visits 
all locations exactly once and returns to the starting point, 
minimizing the overall travel distance.

Name: travellingSalesman.py
Authors: Tiwari
Date Created: 3/15/24
Date Modified: 3/17/24 SAT
Version: 0.0.1
References:
https://www.geeksforgeeks.org/travelling-salesman-problem-using-dynamic-programming/
"""
from sys import maxsize
class TravellingSalesman:
    def __init__(self, distances):
        self.distances = distances  # 2D array with distances between each pair of points
        self.n = len(distances)  # num of points
        self.dp = [[None for _ in range(self.n)] for __ in range(1 << self.n)]
        self.parent = [[None for _ in range(self.n)] for __ in range(1 << self.n)]

    def tsp(self):
        # init table
        for i in range(self.n):
            self.dp[1 << i][i] = self.distances[0][i]
        
        # fill table
        for mask in range(1 << self.n):
            for u in range(self.n):
                if mask & (1 << u):
                    for v in range(self.n):
                        if mask & (1 << v) == 0:
                            next_mask = mask | (1 << v)
                            if self.dp[next_mask][v] is None or self.dp[next_mask][v] > self.dp[mask][u] + self.distances[u][v]:
                                self.dp[next_mask][v] = self.dp[mask][u] + self.distances[u][v]
                                self.parent[next_mask][v] = u

        # reconstruct path
        mask = (1 << self.n) - 1
        u = min(range(self.n), key=lambda i: self.dp[mask][i])
        path = []
        
        while u is not None:
            path.append(u)
            mask, u = mask ^ (1 << u), self.parent[mask][u]

        path.reverse()
        return path, self.dp[(1 << self.n) - 1][path[-1]]

    @staticmethod
    def calculate_distances(debris_locations):
        # Calculate Euclidean distances between debris locations
        # TODO: finishme
        distances = []
        return distances