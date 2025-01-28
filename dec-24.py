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
    
    # get output and generate binary
    # output = {key:val for key, val in vals.items() if re.search("^z[0-9]{2}",key)}
    # reverse_keys = sorted(output,reverse=True)
    # binary = "".join([str(output[i]) for i in reverse_keys])

    # Filter and sort keys, then generate binary
    binary = "".join(
        str(vals[key]) 
        for key in sorted((k for k in vals if k.startswith("z")), reverse=True)
    )

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

    def get_wires(letter:str, values):
        # return {key:val for key, val in values.items() if key.startswith(letter)}
        return [val for key, val in values.items() if key.startswith(letter)]
    
    def sum_wires(wire_a, wire_b):
        out_wire = {}

        for i in range(len(wire_a)):
            a_i, b_i = wire_a[i], wire_b[i]
            c_i = out_wire.get(i,0)

            # ripple carry
            out_wire[i] = a_i ^ b_i ^ c_i
            out_wire[i+1] = (a_i and b_i) or (a_i ^ b_i and c_i)
        
        return list(out_wire.values())
    
    def ripple_carry(a_i,b_i,c_in):
        z_i = a_i ^ b_i ^ c_in
        c_out = (a_i and b_i) or (a_i ^ b_i and c_in)
        return z_i, c_out
    


    # get init x and y
    x_wires, y_wires = get_wires("x",vals), get_wires("y", vals)
    z_wires = sum_wires(x_wires, y_wires)

    # setup output
    z_carry = {0:0}
    z_out = {}
    wrong_insrs = []

    while instructions:

        instr = instructions.pop(0)

        a = vals.get(instr["in"][0],None)
        b = vals.get(instr["in"][2],None)
        
        if a is None or b is None:
            instructions.append(instr)
            continue

        # run operation and save the value
        op = ops[instr["in"][1]]
        vals[instr["out"]] = op(a,b)

        # if set the output bit with an op different from XOR, this doesn't give us the ripple carry 
        if instr["out"].startswith("z") and instr["in"][1] != "XOR":
            wrong_insrs.append(instr)

    return wrong_insrs

    



# RUN


file_name = "data/example.txt"
file_name = "data/dec-24.txt"

vals, instructions = load_data(file_name)
# print(vals, instructions)

# out = read_instructions(vals, instructions)
out = read_instrs_with_extra_steps(vals, instructions)
print(out)