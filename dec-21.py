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

        
        queue = [(np.sum(abs(end_pos - start_pos)), start_pos,[] )] # distance, position, path
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
        paths[(start,end)] = possible_paths

    return paths



def remote_ception(data):

    keypad = np.array([["7","8","9"],["4","5","6"],["1","2","3"],[None,"0","A"]])
    remote_pad = np.array([[None,"^","A"],["<","v",">"]])

    keypad_paths = build_paths(keypad)
    remote_paths = build_paths(remote_pad)
    # print(remote_paths)

    max_iter = 3

    
    sequences = []
    for code in data:
        sequence = []


        queue = [(code, 0)] # chars, position on pad, i (0 to 3)
        visited = set()
        prev_val = "A"


        while queue:
            chars, i = queue.pop()
            # sub_seqs = {}

            if tuple(chars) in visited:
                continue

            visited.add(tuple(chars))

            pad_paths = keypad_paths if i == 0 else remote_paths


            if i == max_iter and (len(chars) < len(sequence) or not sequence):
                sequence = chars 
                continue

            combinations = []

            for j, val in enumerate(chars):
                next_seqs = pad_paths.get((prev_val,val),[["A"]])
                combinations.extend(next_seqs[0])
            
                # combinations = [x + y for x, y in itertools.product(combinations, next_seqs)] if combinations else next_seqs
                prev_val = val       

            queue.append((combinations,i+1))
            # if i< max_iter:
            #     queue.extend(combinations)
            # print(combinations)
            # for comb in combinations:
            #     if i < max_iter:
            #         queue.append((comb, i+1))
            # print(combinations)

            # break
        sequences.append(sequence)
        break


    
    output = 0
    print(sequences)
    for i, seq in enumerate(sequences):
        code = int("".join(data[i][:-1]))
        seq_string = "".join(seq)
        print(code, len(seq), seq_string, )
        output += code * len(seq)

    return output
# RUN

file_name = "data/example.txt"
# file_name = "data/dec-21.txt"

data = load_data(file_name)
out = remote_ception(data)
print(out)
