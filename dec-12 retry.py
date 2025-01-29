from collections import deque
import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 12

def load_data(file_name):
    return [list(line.strip()) for line in open(file_name, "r").readlines()]



# task 1:
#   - compute how much fences would cost
#   - garden plot grows 1 single type of plant, each with a different letter
#   - region formed by group of same plants, horizontaly and vertically connected
#   - copute area and perimeter of each formed region of plants. 
#       Area = # of plants in the region, 
#       perim = number of sides around the region
#   - cost = perim * area


def compute_fencing_cost(data):
    tot_cost = 0

    # get different plant types
    plant_types = set().union(*data)

    # Precompute neighbor offsets (4-directional adjacency)
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    all_clusters = []

    for plant_type in plant_types:
        coords = [(i, j) for i in range(len(data)) for j in range(len(data[i])) if data[i][j] == plant_type]
        
        visited = set()

        for coord in coords:
            if coord in visited:
                continue
            
            queue = deque([coord])           
            new_cluster = []

            while queue:
                x,y = queue.popleft()

                if (x,y) in visited:
                    continue

                visited.add((x,y))
                new_cluster.append((x,y))

                for dx,dy in neighbors:
                    neighbor = (x+dx, y+dy)
                    if neighbor in coords and neighbor not in visited:
                        queue.append(neighbor)

            all_clusters.append(new_cluster)


    print(len(all_clusters))

    return tot_cost


# RUN


file_name = "data/example.txt"
file_name = "data/dec-12.txt"

data = load_data(file_name)

out = compute_fencing_cost(data)


print("tot cost: ", out)
