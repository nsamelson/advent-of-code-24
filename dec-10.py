
import numpy as np
from tqdm import tqdm
import itertools
import re


# DAY 10

def load_data(file_name):
    data = []

    with open(file_name, "r") as f:
        for line in f:
            digits = [int(point) for point in list(line.strip())]
            data.append(digits)
        # data = [line.strip() for line in  f]

    return data


# Task 1:
#   - fill the missing hiking trails
#   - map indicates height of each position (0 to 9)
#   - hiking trail is as long as possible with even gradual uphill slope
#   - starts at 0 and ends at 9, and increases by 1 at each step, up down, left, right
#   - count trailheads = number of peaks (9) we can reach


def count_trailheads(map_data):
    map_array = np.array(map_data)
    valid_paths = 0
    trail_head_scores = {}

    trail_starts = np.column_stack(np.where(map_array == 0))
    
    for start in trail_starts:

        new_pos = start.copy()
        path_history = [new_pos]
        trail_head_scores[str(start)] = []
        

        def find_path(new_pos, trail_height, history=[]):
            if trail_height >= 10:
                if not any(np.all(reached_end == new_pos) for reached_end in trail_head_scores[str(start)]):
                    trail_head_scores[str(start)].append(new_pos)
                return

            # find candidates with the trail_height and compute distance from current position
            trail_candidates = np.column_stack(np.where(map_array == trail_height))
            trail_distances = np.absolute(trail_candidates - new_pos)
            
            # if distance is of 1, then can go through this path
            next_indices = np.where(np.sum(trail_distances,axis=1)==1)

            # failed_path
            if len(next_indices[0]) == 0:
                return

            next_trails = trail_candidates[next_indices[0]]
            
            for pos in next_trails:
                find_path(pos, trail_height + 1, history + [pos])

            return
        
        find_path(new_pos,1, path_history)

    valid_paths = sum([len(y) for x,y in trail_head_scores.items()])
    return valid_paths


# task 2:
#   - check all the individual paths don't care if reach the same end

def count_different_trails(map_data):
    map_array = np.array(map_data)
    valid_paths = 0

    trail_starts = np.column_stack(np.where(map_array == 0))
    
    for start in trail_starts:

        new_pos = start.copy()
        path_history = [new_pos]        

        def find_path(new_pos, trail_height, history=[]):
            valid = 0
            if trail_height >= 10:
                    return 1

            # find candidates with the trail_height and compute distance from current position
            trail_candidates = np.column_stack(np.where(map_array == trail_height))
            trail_distances = np.absolute(trail_candidates - new_pos)
            
            # if distance is of 1, then can go through this path
            next_indices = np.where(np.sum(trail_distances,axis=1)==1)

            # failed_path
            if len(next_indices[0]) == 0:
                return 0

            next_trails = trail_candidates[next_indices[0]]
            
            for pos in next_trails:
                valid += find_path(pos, trail_height + 1, history + [pos])

            return valid
        
        valid_paths += find_path(new_pos,1, path_history)

    return valid_paths

# RUN

file_name = "data/example.txt"
file_name = "data/dec-10.txt"

data = load_data(file_name)

# trailheads = count_trailheads(data)
all_trails = count_different_trails(data)
print(all_trails)

