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
def remote_ception(data):

    keypad = np.array([["7","8","9"],["4","5","6"],["1","2","3"],[None,"0","A"]])
    remote_pad = np.array([[None,"^","A"],["<","v",">"]])

    dirs = [
        [np.array((0,1)), ">"],
        [np.array((1,0)), "v"],
        [np.array((0,-1)), "<"],
        [np.array((-1,0)), "^"]
    ]

    keypad_pos = np.array((3,2))
    rem_pos= np.array((0,2))

    def do_sequence(start_path, start_pos, pad):
        start_dist = abs(start_path[0]) + abs(start_path[1])
        sub_seqs = [] 

        queue = [(start_pos, start_path, start_dist, [])]
        visited = set()

        while queue:
            pos, path, dist, sub_seq = queue.pop(0)
            visited.add(tuple(((pos[0]),pos[1])))

            if dist == 0:
                sub_seqs.append(sub_seq)
                continue

            for dir,seq in dirs:
                new_path = path - dir
                new_pos = pos + dir
                new_dist = abs(new_path[0]) + abs(new_path[1])

                if not 0 <= new_pos[0] < pad.shape[0] or not 0 <= new_pos[1] < pad.shape[1]:
                    continue

                if tuple((new_pos[0],new_pos[1])) in visited:
                    continue

                if (new_dist < dist) and pad[new_pos[0],new_pos[1]]:
                    queue.append((new_pos,new_path,new_dist,sub_seq+[seq]))

        
        return sub_seqs
    
    sequence = []
    for code in data:
        sub_seq = []

        for i in range(4):
            subsub_seq = []

            if i == 0:  # keypad
                chars, pad, pos = [code], keypad, keypad_pos
            else:       # remote pad
                chars, pad, pos = sub_seq, remote_pad, rem_pos

            for possi in chars:
                for val in possi:
                    next_pos = np.argwhere(pad==val)[0]
                    path = next_pos - pos
                    pressed_seq = [item + ["A"] for item in do_sequence(path,pos,pad)]

                    if not subsub_seq:
                        subsub_seq = pressed_seq.copy()
                    else:
                        all_combs = [x + y for x, y in itertools.product(subsub_seq, pressed_seq)]
                        subsub_seq = all_combs.copy()

                    pos = next_pos
                # if i >= 1:
                #     break
            # TODO: Prune a bit more agressively, on the right track but takes too much time
            # Also try maybe BFS in that part 
            lenghts = [len(item) for item in subsub_seq]
            min_len = min(lenghts)
            sub_seq = [item for i, item in enumerate(subsub_seq) if lenghts[i] == min_len]
            # print(sub_seq)
            # if i >= 1:
            #     break
        sequence.append(sub_seq[0])
        break

    
    output = 0
    for i, seq in enumerate(sequence):
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
