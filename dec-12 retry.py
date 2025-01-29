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
    map_array = np.array(data)
    tot_cost = 0

    # get different plant types
    plant_types = set()
    [plant_types.update(line) for line in data]

    for plant_type in plant_types:
        clusters = []
        coords = [[(i, j)] for i in range(len(data)) for j in range(len(data[i])) if data[i][j] == plant_type]
        
        # if only one coordinate found for that plant type
        if len(coords) == 1:
            clusters.append(coords)
            continue

        while coords:
            coord = coords.pop(0)
            cluster = [coords.pop(i) for i,x in enumerate(coords) if abs(sum([x[0] - coord[0], x[1] - coord[1]]))==1]
            cluster.append(coord)

            print(cluster, coords)




        # coords = np.stack(np.where(map_array == plant_type), axis=-1)

        # print(plant_type, coords)

        # coord_0 = coords[0]
        # touching = np.where(abs(np.sum(coords - coord_0,axis=1))==1)
        
        # new_cluster = coords[touching[0]]
        # print(new_cluster)
            

            

        

        break
    

     

    return tot_cost


# RUN


file_name = "data/example.txt"
# file_name = "data/dec-12.txt"

data = load_data(file_name)

out = compute_fencing_cost(data)


print("tot cost: ", out)
