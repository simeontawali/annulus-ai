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
https://www.tutorialspoint.com/data_structures_algorithms/travelling_salesman_problem_dynamic_programming.htm
https://www.baeldung.com/cs/tsp-dynamic-programming
"""

import sys
import numpy as np
class DynamicTSP:
    def __init__(self, distances):
        self.distances = distances  # Distance matrix
        self.n = len(distances)  # Number of nodes/cities
        self.shallow_distance = distances
        #self.dp = [[np.inf for _ in range(self.n)] for __ in range(1 << self.n)]
        #self.parent = [[-1 for _ in range(self.n)] for __ in range(1 << self.n)]

    
def dynamic_tsp(subN, s, cost, visited, distances):
    # intially N = [0 -> len(distances)]
    # intially cost = 0
    # initially visted = [0]*len(N)
    # Have a base case maybe, start from the first city
    # DP to compute minimum cost
    # Reconstruct path
    visited[s] = 1
    if(len(subN) == 2 and subN[-1] != s):
        cost += distances[subN[0]][subN[1]]
        return cost
    else:
        min_paths = []
        for i in subN:
            min_paths.append(dynamic_tsp(subN.remove(s), i, cost, visited, distances))
    return cost