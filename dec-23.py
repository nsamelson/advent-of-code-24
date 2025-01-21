from collections import defaultdict, deque
import heapq
import math
# import numpy as np
# from tqdm import tqdm
from itertools import chain, product, combinations
import re
from functools import cache, lru_cache

# DAY 23 LAN party


def load_data(file_name):
    return [set((line.strip()).split("-")) for line in open(file_name).readlines()]


# task 1:
#   - input is a list of connection between 2 computers, which are BI-directional
#   - find sets of 3 connected computers
#   - count sets where at least one of the connected computers STARTS with a "t" (e.g. "tc")

def triconnect(data):

    connected = []
    
    # generate set of all different computers with "t" in it
    chief_set = set(item for sub_item in data for item in sub_item if "t" == item[0])
   
    
    # iterate over the chief potential computers
    for chief in chief_set:
        
        chief_conns = [item for sub_item in data for item in sub_item if chief in sub_item and chief!= item]
        conn_combs = list(combinations(chief_conns,2))

        filtered = [set(conn + (chief,)) for conn in conn_combs if set(conn) in data]
        [connected.append(subset) for subset in filtered if subset not in connected]

    return len(connected)




# task 2:








# RUN


file_name = "data/example.txt"
file_name = "data/dec-23.txt"

data = load_data(file_name)
# print(data)

out = triconnect(data)
print(out)
