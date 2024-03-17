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

import sys
import numpy as np
class DynamicTSP:
    def __init__(self, distances):
        self.distances = distances  # Distance matrix
        self.n = len(distances)  # Number of nodes/cities
        #self.dp = [[np.inf for _ in range(self.n)] for __ in range(1 << self.n)]
        #self.parent = [[-1 for _ in range(self.n)] for __ in range(1 << self.n)]

    def dynamic_tsp(distances, debris_locations):
        # Have a base case maybe, start from the first city
        # DP to compute minimum cost
        shallow_dis = distances
        # Reconstruct path
        node_path = [0]
        #cost = 0
        for liss in shallow_dis:
            for dis in liss:
                to_next = liss.index(min(liss))
                if(to_next in node_path):
                    liss[to_next] = sys.maxsize
                else:
                    #cost += liss[to_next]
                    node_path.append(to_next)
                    break
        node_path.append(0)

        path = []

        for node in node_path:
            path.append(debris_locations[node])

        print(path)
        #print(cost)
        return path #, cost
    
    
    
    






