from collections import defaultdict, deque
import heapq
import math
# import numpy as np
# from tqdm import tqdm
from itertools import chain, product, combinations
import re
from functools import cache, lru_cache
import networkx as nx

# DAY 25 code chronicle

def load_data(file_name):
    keys, locks = [],[]
    is_lock = False
    temp_pad = []

    i = 0
    for line in open(file_name).readlines():
        line = line.strip()

        if not line:
            continue

        # first line
        if i==0:
            is_lock = True if "#" in line and "." not in line else False
            temp_pad = [0] * 5
            i+=1
        elif i == 6:
            locks.append(temp_pad) if is_lock else keys.append(temp_pad)
            temp_pad = []
            i=0
        else:
            temp_pad = [val + 1 if line[j]=="#" else val for j,val in enumerate(temp_pad)]
            i+=1   

    return keys, locks


def find_fitting_keys(keys, locks):

    combs = product(keys, locks)
    fit_count = 0
    
    for key, lock in combs:
        fitting = [x + y <6 for x, y in zip(key, lock)]
        
        if all(fitting):
            fit_count+=1


    return fit_count









# RUN


file_name = "data/example.txt"
file_name = "data/dec-25.txt"

keys, locks = load_data(file_name)
out = find_fitting_keys(keys, locks)

print(out)
