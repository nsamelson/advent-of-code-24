from collections import deque
import heapq
import math
import numpy as np
from tqdm import tqdm
from itertools import chain, product
import re

# DAY 21 Keypad Conundrum


def load_data(file_name):
    data = [list(line.strip() )for line in open(file_name).readlines()]

    return data


# Task 1:
#   - guide robot to enter code, guide it with directional keys + A for activation
#   - start from bottom right of code keypad
#   - multiple ways to go from button to button
#   - you control a robot that controls a robot that controls a robot that enters the keycode
#   - find shortest sequence of button presses, complexity = length of sequence * numeric part of the code

import itertools

def build_paths(pad):
    paths = {}
    distances = {}
    values = pad.flatten()
    combs = list(itertools.product(values, values))

    dirs = [
        [np.array((0,1)), ">"],
        [np.array((1,0)), "v"],
        [np.array((0,-1)), "<"],
        [np.array((-1,0)), "^"]
    ]
    
    for (start,end) in combs:
        # skip invalid paths
        if not start or not end or start == end:
            continue

        start_pos = np.argwhere(pad==start)[0]
        end_pos = np.argwhere(pad==end)[0]
        dist = np.sum(abs(end_pos - start_pos))

        
        queue = [(dist, start_pos,[] )] # distance, position, path
        visited = set()
        possible_paths = []

        while queue:
            dist, pos, path = queue.pop(0)
            
            visited.add(tuple(pos))

            if np.all(pos == end_pos):
                possible_paths.append(path+["A"])
                continue

            for dir,char in dirs:
                new_pos = pos + dir
                new_dist = np.sum(abs(end_pos - new_pos))

                if new_dist>= dist: 
                    continue
                if not 0 <= new_pos[0] < pad.shape[0] or not 0 <= new_pos[1] < pad.shape[1]:
                    continue
                if tuple(new_pos) in visited:
                    continue

                if pad[new_pos[0],new_pos[1]]:
                    new_path = path.copy() + [char]
                    queue.append((dist, new_pos,new_path))
        
        # keep only the ones that group the repeated moves
        moves_per_path = []
        for path in possible_paths:
            moves = sum([1 if path[i-1] != path[i] else 0 for i in range(1, len(path))])
            moves_per_path.append(moves)

        min_moves = min(moves_per_path)

        paths[(start,end)] = tuple((tuple(path) for i,path in enumerate(possible_paths) if moves_per_path[i]==min_moves))
        distances[(start,end)] = dist
        

    return paths, distances


def remote_ception(data):

    keypad = np.array([["7","8","9"],["4","5","6"],["1","2","3"],[None,"0","A"]])
    remote_pad = np.array([[None,"^","A"],["<","v",">"]])

    keypad_paths, keypad_dists = build_paths(keypad)
    remote_paths, remote_dists = build_paths(remote_pad)

    # recursive func
    def get_seq(code,i):
        pad_paths = keypad_paths if i == 0 else remote_paths
        prev_val = "A"

        # if reach the max depth, return
        if i == 3:
            return code

        combinations = []
        for j,val in enumerate(code):
            # get the sequence between 2 values
            seq_val = pad_paths.get((prev_val,val),[["A"]]) 
            prev_val = val           

            # generate all sequences recursively
            new_seqs = [get_seq(path,i+1) for path in seq_val]

            # create all possible combinations
            combinations = [x+y for x,y in itertools.product(combinations, new_seqs)] if combinations else new_seqs

        # filter to get the min
        cost_per_comb = []
        for comb in combinations:
            cost_per_comb.append(sum([remote_dists.get(("A" if i==0 else comb[i-1],comb[i]),0) for i in range(0,len(comb))]))
        min_index = cost_per_comb.index(np.min(cost_per_comb,axis=0))


        return combinations[min_index]    

    # iterate over all codes
    sequences = []
    for code in data:
        sequences.append(get_seq(code, 0))
    
    # compute move cost
    output = 0
    for i, seq in enumerate(sequences):
        code = int("".join(data[i][:-1]))
        seq_string = "".join(seq)
        print(code, len(seq), seq_string, )
        output += code * len(seq)

    return output

# Task 2: now there are 25 robots instead of 3

from functools import lru_cache, cache
MAX_DEPTH = 12

def remote_ception_cached(data):
    # Ensure data is hashable (convert from list to tuple)
    data = tuple(tuple(x) for x in data)  # Convert each sublist to a tuple

    keypad = np.array([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]])
    remote_pad = np.array([[None, "^", "A"], ["<", "v", ">"]])

    keypad_paths, keypad_dists = build_paths(keypad)
    remote_paths, remote_dists = build_paths(remote_pad)


    @lru_cache(maxsize=None)
    def get_seq_cost(code):
        return sum(remote_dists.get(("A" if i == 0 else code[i - 1], code[i]), 0) for i in range(len(code)))

    # Recursive function
    @lru_cache(maxsize=None)
    def get_seq(code, i):
        pad_paths = keypad_paths if i == 0 else remote_paths
        prev_val = "A"

        # If reach the max depth, return
        if i == MAX_DEPTH:
            return code

        combinations = ()
        for j, val in enumerate(code):
            # Get the sequence between 2 values
            seq_val = pad_paths.get((prev_val, val), tuple((("A",),)))
            prev_val = val           

            # Generate all sequences recursively
            new_seqs = tuple(get_seq(path, i + 1) for path in seq_val)

            # Create all possible combinations
            combinations = tuple(x + y for x, y in itertools.product(combinations, new_seqs)) if combinations else new_seqs

        return min(combinations, key=lambda comb: get_seq_cost(comb))

    # Iterate over all codes
    sequences = [get_seq(code, 0) for code in data]
    
    # Compute move cost
    output = 0
    for i, seq in enumerate(sequences):
        code = int("".join(data[i][:-1]))
        output += code * len(seq)

    return output









# RUN

file_name = "data/example.txt"
file_name = "data/dec-21.txt"

data = load_data(file_name)
# out = remote_ception(data)
out = remote_ception_cached(data)
print(out)
