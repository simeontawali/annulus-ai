"""
Dynamic Programming for TSP: Solve the TSP using Dynamic 
Programming to ensure an optimal solution. Break down the problem 
into smaller subproblems and solving each exactly once, 
storing the results for future use (multiple runs).

Authors: Yuen
Date Created: 3/15/24
Date Modified: 3/15/24 SAT
Version: 0.0.1
References:
https://www.geeksforgeeks.org/travelling-salesman-problem-using-dynamic-programming/
"""
import numpy as np
class DynamicTSP:
    def __init__(self, distances):
        self.distances = distances  # Distance matrix
        self.n = len(distances)  # Number of nodes/cities
        self.dp = [[np.inf for _ in range(self.n)] for __ in range(1 << self.n)]
        self.parent = [[-1 for _ in range(self.n)] for __ in range(1 << self.n)]

    def dynamic_tsp(self):
        # Have a base case maybe, start from the first city
        # DP to compute minimum cost
        # Reconstruct path
        path = None
        cost = 0
        return path, cost


    @staticmethod
    def calculate_distances(locations):
        # Calculate Euclidean distances between locations
        # TODO: finish me
        distances = []
        return distances




