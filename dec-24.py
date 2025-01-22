# from collections import defaultdict, deque
# import heapq
# import math
# import numpy as np
# from tqdm import tqdm
# from itertools import chain, product, combinations
import re
# from functools import cache, lru_cache
# import networkx as nx

# DAY 24 crossed wires


def load_data(file_name):
    vals = {}
    instructions = []

    for line in open(file_name).readlines():
        line = line.strip()

        if ":" in line:
            val = line.split(":")
            vals[val[0]] = int(val[1])

        if "->" in line:
            val = line.split(" ")
            instructions.append({
                "in": val[0:3],
                "out":val[-1]
            })

    return vals, instructions




# task 1
import operator

def read_instructions(vals, instructions:list):

    ops = {
        "AND": operator.and_,
        "OR": operator.or_,
        "XOR": operator.xor,
    }

    # for instr in instructions:

    while instructions:
        instr = instructions.pop(0)

        a = vals.get(instr["in"][0],None)
        b = vals.get(instr["in"][2],None)

        if a is None or b is None:
            instructions.append(instr)
            continue

        op = ops[instr["in"][1]]

        # run operation and save the value
        vals[instr["out"]] = op(a,b)

    print(len(vals), vals)
    
    # get output and generate binary
    output = {key:val for key, val in vals.items() if re.search("^z[0-9]{2}",key)}
    reverse_keys = sorted(output,reverse=True)
    binary = "".join([str(output[i]) for i in reverse_keys])

    print(binary)

    return int(binary,2)




# task 2:
#   - wires starting with x as one binary #, wires starting with y as a second binary #, then adding those 2 together
#   - output of this operation is set on wires starting with z
#   - 4 pairs of gates have been swapped (one swap each)

def read_instrs_with_extra_steps(vals, instructions:list):
    ops = {
        "AND": operator.and_,
        "OR": operator.or_,
        "XOR": operator.xor,
    }



# RUN


file_name = "data/example.txt"
# file_name = "data/dec-24.txt"

vals, instructions = load_data(file_name)
# print(vals, instructions)

out = read_instructions(vals, instructions)
out = read_instrs_with_extra_steps(vals, instructions)
print(out)