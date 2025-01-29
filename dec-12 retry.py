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


def get_clusters(data):
    rows, cols = len(data), len(data[0])

    # Precompute neighbor offsets (4-directional adjacency)
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()

    def bfs(coord):
        queue = deque([coord])
        cluster = []

        while queue:
            x,y = queue.popleft()
            plant = data[x][y]
            if (x,y) in visited:
                continue

            visited.add((x,y))
            cluster.append((x,y))

            for dx,dy in neighbors:
                nx,ny = (x+dx, y+dy)
                if 0 <= nx < rows and 0 <= ny < cols:
                    if data[nx][ny]==plant and (nx,ny) not in visited:
                        queue.append((nx,ny))
        return cluster

    # BIM!!!
    return [bfs((i,j)) for i in range(rows) for j in range(cols) if (i,j) not in visited]

def compute_fencing_cost(data):
    clusters = get_clusters(data)
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    tot_cost = 0

    for cluster in clusters:
        area = len(cluster)
        perimeter = 0

        for (x,y) in cluster:
            perimeter += sum([1 for dx,dy in neighbors if (x+dx, y+dy) not in cluster])

        tot_cost += area * perimeter

    return tot_cost

# Task 2:
#   - count number of contiguous sides

def compute_bulk_cost(data):
    clusters = get_clusters(data)
    row_neighbors = [(0, -1), (0, 1)]
    col_neighbors = [(-1, 0), (1, 0)]
    

    def bfs(visited, cluster, coord, neighbors):
        queue = [coord]
        sub_cluster = []

        while queue:
            x,y = queue.pop(0)

            if (x,y) in visited:
                continue

            visited.add((x,y))
            sub_cluster.append((x,y))

            for dx,dy in neighbors:
                nx,ny = (x+dx, y+dy)
                if (nx,ny) in cluster and (nx,ny) not in visited:
                    queue.append((nx,ny))

        return sub_cluster, visited


    tot_cost = 0
    for cluster in clusters:
        area = len(cluster)
        perimeter = 0

        h_visited = set()
        v_visited = set()

        for coord in cluster:
            sides = []

            # check horizontal sub_clusters
            if coord not in h_visited:
                horiz_cluster, h_visited = bfs(h_visited,cluster,coord,row_neighbors)
                # find free top and bottom sides
                sides.extend([[(x+dx, y+dy) not in cluster for x,y in horiz_cluster ] for dx,dy in col_neighbors ])

            # check vertical sub_clusters
            if coord not in v_visited:
                vert_cluster, v_visited = bfs(v_visited,cluster,coord,col_neighbors)
                # find free left and right sides
                sides.extend([[(x+dx, y+dy) not in cluster for  x,y in vert_cluster ] for dx,dy in row_neighbors])
                
            # Count the number of grouped True statements [True,True,False,True] = 2 groups = 2 free sides
            perimeter += sum([len([list(j) for i,j in itertools.groupby(side) if i==True]) for side in sides])

        tot_cost += area * perimeter
        # print(cluster, area, perimeter, area * perimeter)
    
    return tot_cost



# RUN


file_name = "data/example.txt"
# file_name = "data/dec-12.txt"

data = load_data(file_name)

# out = compute_fencing_cost(data)
out = compute_bulk_cost(data)


print("tot cost: ", out)
