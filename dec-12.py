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
def cluster_plants_bfs(data):
    tot_cost = 0

    map_array = np.array(data)
    rows, cols = map_array.shape

    visited = np.zeros_like(map_array, dtype=bool)
    clusters = []

    def bfs(start):
        cluster = []
        queue = [start]
        visited[start] = True
        # print(visited)

        while queue:
            row, col = queue.pop(0)
            cluster.append((row, col))

            # get mini array of all neighbours
            # Check all 4 neighbors (up, down, left, right)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                
                # Check bounds and ensure valid neighbour
                if (0 <= nr < rows and 0 <= nc < cols and 
                        not visited[nr][nc] and map_array[nr][nc] == map_array[row][col]):
                    visited[nr][nc] = True
                    queue.append((nr, nc))

        return cluster
    
    # iterate through the array
    for r in range(rows):
        for c in range(cols):
            if not visited[r,c]:
                clusters.append(bfs((r,c)))
    
    return clusters


# def count_fence_costs(clusters):
#     tot_cost = 0

#     for i,cluster in enumerate(clusters):
#         area = len(cluster)
#         perim = [4 - len(np.where(np.sum(abs(cluster - coord), axis=1) == 1)[0]) for coord in np.array(cluster)]
#         tot_cost += area * sum(perim)   

#     return tot_cost

def count_fence_costs(clusters):
    tot_cost = 0

    for cluster in clusters:
        cluster_set = set(cluster)  # Convert to set for O(1) lookups
        area = len(cluster)
        perimeter = 0

        for x, y in cluster:
            # Check each neighbor
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            free_sides = sum(1 for n in neighbors if n not in cluster_set)
            perimeter += free_sides

        tot_cost += area * perimeter

    return tot_cost

# Task 2:
#   - count number of contiguous sides

def count_discount(clusters):
    tot_cost = 0

    for cluster in clusters:
        area = len(cluster)
        perimeter = 0

        # pad the cluster
        cluster = [(x+1,y+1) for x,y in cluster]
        cluster_set = set(cluster)

        # get free edges
        free_edges = []
        for x,y in cluster:
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            free_edges.extend([n for n in neighbors if n not in cluster_set])

        free_edges_set = set(free_edges)
        grouped_edges = []
        h_lines = []
        v_lines = []
        single_edges = []

        # visited = np.zeros_like(free_edges_set, dtype=bool)

        for edge in free_edges_set:
            x,y = edge
            repeat = free_edges.count(edge)
            h_neighbors = [(x, y + 1), (x, y - 1)]
            v_neighbors = [(x + 1, y), (x - 1, y)]
            
            connected_h = [n for n in h_neighbors if n in free_edges_set]
            connected_v = [n for n in v_neighbors if n in free_edges_set]

            if len(connected_h) !=0:
                connected_h.append(edge)
                
                indices = [i for i,connected in enumerate(h_lines) if any(e in connected for e in connected_h)]
                if len(indices) == 0:
                    h_lines.append(set(connected_h))
                elif len(indices) == 1:
                    h_lines[indices[0]].update(connected_h)
                else:
                    h_lines[indices[0]].update(connected_h)
                    # h_lines[indices[1]].update(connected_h)
                    h_lines.pop(indices[1])
                print(repeat)
        print(h_lines, )

                # print(h_lines)

            # if len(connect_edge)==0:
            #     perimeter +=1
            
            # if repeat == 1:
            #     perimeter +=1

            # if repeat >1:
            #     print(edge, repeat)

        print(area , perimeter)
        # group edges

        # peri_coords = []
        # clustered_coords = []

        # for coord in padded_cluster:
        #     for dist in np.array([(-1, 0), (1, 0), (0, -1), (0, 1)]):
        #         neighbour = coord + dist
        #         if np.all(np.all(neighbour == padded_cluster, axis=1)==False):
        #             peri_coords.append(neighbour)

        # print(peri_coords)
        tot_cost += area * perimeter
    
    return tot_cost

# RUN


file_name = "data/example.txt"
file_name = "data/dec-12.txt"

data, plants = load_data(file_name)
# cost = compute_fencing_cost(data, plants)

clusters = cluster_plants_bfs(data)
# print(len(clusters))
# cost = count_fence_costs(clusters)
# cost = count_discount(clusters)

# print("tot cost: ", cost)
