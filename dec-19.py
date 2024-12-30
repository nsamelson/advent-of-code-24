from collections import deque
import heapq
import math
import numpy as np
from tqdm import tqdm
from itertools import chain
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

    def find_combinations(indices):
        """Create all possible combinations by merging indices together if they're following
        Examples:
            - (0,1) and (1,2) are following up ==> add a new (0,2) in the set
            - (0,1) and (0,3) don't follow up ==> add a new (0,3) in the set
        """
        merged = set()

        for start,end in indices:
            # find ends in merged that == start            
            new_starts = [x for (x,y) in merged if y==start]

            if new_starts:
                for val in new_starts:
                    merged.add((val, end))            
            else:
                merged.add((start,end))
            
        return merged

    for string in designs:
        valid_range = (0,len(string))
        found_indices = set()

        # find for each pattern, the indices of found match in string
        for pattern in patterns:
            indices = [(m.start(0), m.end(0)) for m in re.finditer(pattern, string)]
            
            if indices:
                found_indices.update(indices)
        
        combinations = find_combinations(sorted(found_indices))

        if valid_range in combinations:
            possible_combs +=1        
        
    return possible_combs


# this one's better
def linen_regex(patterns, designs):
    possible_combs = 0

    valid_patterns = r"^(" + "|".join(patterns) + ")+$"
    
    for string in designs:
        matching = re.match(valid_patterns, string)

        if matching:
            possible_combs+=1

    return possible_combs


# Task 2:
#   - find all possible combinations of towel arrangements

# import regex as re

def linen_combinations(patterns, designs):
    possible_combs = 0

    def count_combs(ranges, valid_range):
        combs = []

        for x,y in ranges:
            new_combs = [(i,y) for (i,j) in combs if j==x]
            if new_combs:
                combs.extend(new_combs)
            else:
                combs.append((x,y))
        
        return combs.count(valid_range)

    for string in designs:
        valid_range = (0,len(string))

        ranges = [(m.start(0), m.end(0)) for pattern in patterns for m in re.finditer(pattern, string)]
        
        possible_combs+= count_combs(sorted(ranges), valid_range)

    return possible_combs

# RUN

file_name = "data/example.txt"
file_name = "data/dec-19.txt"

patterns, designs = load_data(file_name)

out = linen_regex(patterns, designs)
out = linen_combinations(patterns, designs)
print(out)
