import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 12

def load_data(file_name):
    data = []
    plant_set = set()

    with open(file_name, "r") as f:
        for line in f:
            line = list(line.strip())
            data.append(line)
            plant_set.update(line)

    return data, plant_set

# task 1:
#   - compute how much fences would cost
#   - garden plot grows 1 single type of plant, each with a different letter
#   - region formed by group of same plants, horizontaly and vertically connected
#   - copute area and perimeter of each formed region of plants. 
#       Area = # of plants in the region, 
#       perim = number of sides around the region
#   - cost = perim * area


def compute_fencing_cost(data, plants):
    map_array = np.array(data)
    tot_cost = 0

    plant_coords = {plant: np.column_stack(np.where(map_array==plant)) for plant in plants}

    for plant_type, coords in plant_coords.items():

        # in case there is only one plant
        if len(coords) == 1:
            tot_cost += 4 # 1 * 4
            continue
        
        # setup first cluster
        clusters = [[coords[0]]]

        for i in range(1,len(coords)):
            coord = coords[i]
            distance_to_coords = [np.any(np.sum(abs(cluster - coord), axis=1) == 1, axis= 0) for cluster in clusters]
            cluster_index =  np.where(distance_to_coords)[0]

            # lone plant
            if len(cluster_index) == 0:
                clusters.append([coord])
            # found in one cluster
            elif len(cluster_index) == 1:
                clusters[cluster_index[0]].append(coord)
            # found in 2 clusters, so join the clusters together
            else:
                clusters[cluster_index[0]] += clusters[cluster_index[1]]
                clusters[cluster_index[0]].append(coord)
                clusters.pop(cluster_index[1])
                
        # compute cost
        for i,cluster in enumerate(clusters):
            area = len(cluster)
            no_neighbours = [4 - len(np.where(np.sum(abs(cluster - coord), axis=1) == 1)[0]) for coord in cluster]
            tot_cost += area * sum(no_neighbours)               

    return tot_cost


# BFS algorithm
def fence_cost_bfs(data, plants):
    map_array = np.array(data)
    tot_cost = 0

    plant_coords = {plant: np.column_stack(np.where(map_array==plant)) for plant in plants}


# RUN


file_name = "data/example.txt"
file_name = "data/dec-12.txt"

data, plants = load_data(file_name)
cost = compute_fencing_cost(data, plants)

print("tot cost: ", cost)
