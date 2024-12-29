from collections import deque
import heapq
import math
import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 18


def load_data(file_name):
    coords = [line.strip().split(",") for line in open(file_name).readlines()]
    int_coords = [(int(a),int(b)) for a,b in coords]            

    return int_coords


# Task 1:
#   - byte falls into memory space every ns
#   - mem space 2D grid range from 0 to 70, given X,Y coordinates and 0,0 in top left
#   - exit to 70,70 in bottom right

def escape_maze(corrupted_coords, bound, bytes):
    start_coord = (0, 0)
    end_coord = (bound,bound)

    queue = deque([(start_coord, [start_coord])])  
    visited = set()

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end_coord:
            return len(path) - 1
        
        if (x, y) in visited:
            continue
        visited.add((x,y))

        for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            n_x, n_y = x + i, y + j

            # Check boundaries and skip invalid or visited nodes
            if 0 <= n_x <= bound and 0 <= n_y <= bound and (n_x, n_y) not in corrupted_coords[:bytes]:
                new_path = path + [(n_x, n_y)]
                queue.append(((n_x, n_y),new_path))


    return None

# Task 2:
#   - how many corrupted bytes will block the maze?

def run_maze(corrupted_coords, bound, bytes):

    def quick_maze(corrupted_coords, bound, bytes):
        start_coord = (bound,bound)
        end_coord = (0,0)

        queue = deque([start_coord])  
        visited = set()

        while queue:
            (x, y) = queue.popleft()

            if (x, y) == end_coord:
                return True
            
            if (x, y) in visited:
                continue

            visited.add((x,y))

            for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                n_x, n_y = x + i, y + j

                # Check boundaries and skip invalid or visited nodes
                if 0 <= n_x <= bound and 0 <= n_y <= bound and (n_x, n_y) not in corrupted_coords[:bytes]:
                    queue.append((n_x, n_y))


        return False

    for i in list(range(bytes,len(corrupted_coords)))[::-1]:
        len_path = quick_maze(corrupted_coords, bound, i)
        # print(i, len_path)

        if len_path:
            blocking_coords = corrupted_coords[i]
            return blocking_coords
        


# RUN

file_name = "data/example.txt"
file_name = "data/dec-18.txt"

coords = load_data(file_name)

# shortest = escape_maze(coords,70,1024)
max_bytes = run_maze(coords,70,1024)
print(max_bytes)
