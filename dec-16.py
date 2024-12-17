import math
import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 16 Reindeer maze

def load_data(file_name):
    map = []

    with open(file_name, "r") as f:
        for line in f:
            line = list(line.strip())

            if len(line)==0:
                continue

            map.append(line)
        
    return map

# tasks:
#   - find lowest path score
#   - start marked S and end marked E, deer facing east
#   - moving 1 forward = 1 point, rotating 90° = 1000 points
import sys
sys.setrecursionlimit(10**3)


directions = {
    "v": np.array([1,0]),
    "^": np.array([-1,0]),
    ">": np.array([0,1]),
    "<": np.array([0,-1]),
}
# rotate_right = np.array([[0, 1],[-1, 0]]) # turn 90 degrees to the right

start_sign= ">"

def maze_dfs(map):
    
    map_array = np.array(map)
    start = np.column_stack(np.where(map_array=="S"))[0]
    min_cost = float('inf')

    def DFS(pos, dir, cost, visited):
        nonlocal min_cost
        x,y = int(pos[0]), int(pos[1])

        if map_array[x,y] == "E":
            print(cost, min_cost)
            min_cost = min(min_cost, cost)
            return

        visited.add((x,y))

        for next_sign, next_dir in directions.items():
            next_pos = pos + next_dir
            i,j = int(next_pos[0]), int(next_pos[1])

            # don't overshoot
            if i < 0 or i >= map_array.shape[0] or j < 0 or j >= map_array.shape[1]:
                continue
            # don't go into walls or go backwards
            if map_array[i,j] == "#" or (i,j) in visited:
                continue
            
            new_cost = cost + (1 if np.all(dir == next_dir) else 1001)

            # don't bother exploring if the cost is bigger than what we already found
            if new_cost >= min_cost:
                continue

            # sneaky bastard don't forget .copy()
            # recursion
            DFS(next_pos, next_dir, new_cost, visited.copy())
    
    DFS(start, directions[start_sign], 0, set())

    return min_cost


import heapq
    
def maze_bfs(map):
    directions = {
        (1, 0): "v",   # down
        (-1, 0): "^",  # up
        (0, 1): ">",   # right
        (0, -1): "<"   # left
    }
    
    map_array = np.array(map)
    min_cost = float('inf')

    # set start as tuple and start dir
    start = tuple(np.column_stack(np.where(map_array == "S"))[0].tolist())
    start_dir = (0, 1)

    visited = set()

    # setup queue and stuff
    queue = [(0, start, start_dir)]  # cost, position, direction
    heapq.heapify(queue)

    # BFS loop
    while queue:

        # Dijkstra banger
        # checks the queue element with the cheapest cost
        cost, (x, y), dir = heapq.heappop(queue)

        if map_array[x,y] == "E":
            print(cost, min_cost)
            min_cost = min(min_cost, cost)
            continue

        # Mark current state as visited
        if ((x, y), dir) in visited:
            continue

        visited.add(((x, y), dir))

        for next_dir in directions.keys():
            next_pos = (x + next_dir[0], y + next_dir[1])
            i,j = next_pos

            # Check if next position is valid
            if not (0 <= i < map_array.shape[0] and 0 <= j < map_array.shape[1]):
                continue
            if map_array[i, j] == "#":
                continue

            # compute new cost of moving
            new_cost = cost + (1 if dir==next_dir else 1001)

            # if overshoots the min cost, don't explore further
            if new_cost >= min_cost:
                continue

            heapq.heappush(queue, (new_cost, next_pos, next_dir))


    return min_cost



# Task 2: skibidi toilet
#   - every non-wall tile is equipped with seat
#   - want to find count number of seats the path takes?

def comfy_maze_bfs(map):
    directions = {
        (1, 0): "v",   # down
        (-1, 0): "^",  # up
        (0, 1): ">",   # right
        (0, -1): "<"   # left
    }
    
    map_array = np.array(map)
    min_cost = float('inf')

    # set start as tuple and start dir
    start = tuple(np.column_stack(np.where(map_array == "S"))[0].tolist())
    start_dir = (0, 1)

    # setup queue and stuff
    queue = [(0, start, start_dir, set())]  # cost, position, direction
    heapq.heapify(queue)

    comfy_path = set()

    # BFS loop
    while queue:

        # Dijkstra banger
        # checks the queue element with the cheapest cost
        cost, (x, y), dir, path = heapq.heappop(queue)

        # Mark current state as visited
        if (x,y) in path:
            continue
       
        # update path
        path.add((x,y))

        if map_array[x,y] == "E":
            min_cost = min(min_cost, cost)
            if min_cost == cost:
                comfy_path.update(path)
            continue

        for next_dir in directions.keys():
            next_pos = (x + next_dir[0], y + next_dir[1])
            i,j = next_pos

            # Check if next position is valid
            if not (0 <= i < map_array.shape[0] and 0 <= j < map_array.shape[1]):
                continue
            if map_array[i, j] == "#":
                continue

            # compute new cost of moving
            new_cost = cost + (1 if dir==next_dir else 1001)

            # if overshoots the min cost, don't explore further
            if new_cost > min_cost:
                continue

            heapq.heappush(queue, (new_cost, next_pos, next_dir, path.copy()))

    return len(comfy_path)



# RUN   


file_name = "data/example.txt"
# file_name = "data/dec-16.txt"

map = load_data(file_name)
# score = maze_bfs(map)
score = comfy_maze_bfs(map)

print(score)

