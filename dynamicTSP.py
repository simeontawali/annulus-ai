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

    
def dynamic_tsp(N, s, cost, visited, distances):
    # intially N = [0 -> len(distances)]
    # intially cost = 0
    # initially visted = [0]*len(N)
    # Have a base case maybe, start from the first city
    # DP to compute minimum cost
    # Reconstruct path
    visited[s] = 1
    if (len(N) == 2 and N[-1] != s):
        cost += distances[N[0]] + distances[N[1]]
        return cost
    else:
        for j in N:
            min_paths = []
            for i in N:
                    if(visited[i] == 0 and j != i and j != s):
                        min_paths.append(dynamic_tsp(N.remove(i), j, cost, visited, distances) + distances[j][i])
                        visited[j] = 1
            return cost


