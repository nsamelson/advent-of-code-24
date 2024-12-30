from collections import deque
import heapq
import math
import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 19 hot springs


def load_data(file_name):
    all_data = [line.strip() for line in open(file_name).readlines()]

    patterns = all_data[0].split(", ")
    designs = all_data[2:]

    return patterns, designs






# Task 1:
#   color patterns: w=white, u=blue, b=black, r=red, g=green
#   need to display all the desired designs from the towel patterns we have by putting them next to eachother


def linen_layout(patterns, designs):
    possible_combs = 0

    # print(sorted(patterns))
    for linup in designs:
        
        is_found = [False] * len(linup)
        i = 0
        while i < len(linup):

            for j in range(1,len(linup)):
                word = linup[i:i+j]

                if word in patterns:
                    is_found[i:i+j] = [True] * j                    
                    break
            i+=j
        print(linup, is_found)
        if all(is_found):
            possible_combs += 1
        # break
        
    return possible_combs





# RUN

file_name = "data/example.txt"
# file_name = "data/dec-19.txt"

patterns, designs = load_data(file_name)

out = linen_layout(patterns, designs)
print(out)
