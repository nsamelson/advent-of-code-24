from collections import deque
import heapq
import math
import numpy as np
from tqdm import tqdm
from itertools import chain, product
import re

# DAY 20 Racing


def load_data(file_name):
    data = [list(line.strip() )for line in open(file_name).readlines()]

    return data


# Task 1: 
#   - tracks = ".", start = "S", end = "E", walls = "#"
#   - each move equals a picosecond, need to reach the end as fast as possible
#   - can cheat ONCE: disable collision with walls for up to 2 moves
#   - how many cheats would save me at least 100 moves?

def race_n_cheat(data):
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]

    # setup map n stuff
    map_array = np.array(data)
    start = np.column_stack(np.where(map_array=="S"))[0]
    end = np.column_stack(np.where(map_array=="E"))[0]
    
    # transform to tuples
    start = tuple(int(x) for x in start)
    end = tuple(int(x) for x in end)
    
    # basic path:
    base_path = []
    queue = [(start,(0,0))] # current, prev

    while queue:
        pos, prev_pos = (x,y),(a,b) = queue.pop(0)
        base_path.append(pos)

        for i,j in dirs:
            next_pos = (x+i, y+j)

            if next_pos == prev_pos:
                continue

            if map_array[next_pos[0],next_pos[1]] == "." or next_pos == end:
                queue.append((next_pos,pos))

    cheat_dirs = [(0,2),(2,0),(0,-2),(-2,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    # now activate cheats
    cheats = []
    for i,pos in enumerate(base_path):
        x,y = pos

        for k,l in cheat_dirs:
            jumped = (x+k,y+l)

            # if fall further into the path, then we successfully cheated
            if jumped in base_path[i:]:
                new_index = base_path[i:].index(jumped)

                if new_index>100:
                    cheats.append(new_index-2)

    return len(cheats)
            
            



# RUN

file_name = "data/example.txt"
# file_name = "data/dec-20.txt"

data = load_data(file_name)
out = race_n_cheat(data)

print(out)