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

class Slam:
    def __init__(self):
        self.objects = []
        self.num_objects = 0
