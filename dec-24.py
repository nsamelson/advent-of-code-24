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

def load_data(file_name):
    vals = {}
    instructions = {}

    for line in open(file_name).readlines():
        line = line.strip()

        if ":" in line:
            val = line.split(":")
            vals[val[0]] = int(val[1])

        if "->" in line:
            val = line.split(" ")
            instructions[val[-1]] = {
                "a": val[0],
                "b": val[2],
                "op":val[1]
            }

    return vals, instructions


def read_instrs_with_extra_steps(vals, instructions:list):
    ops = {
        "AND": operator.and_,
        "OR": operator.or_,
        "XOR": operator.xor,
    }

    def do_op_from_key(out_key):
        instr_i = instructions[out_key]
        a_key, b_key, op_key = instr_i["a"], instr_i["b"], instr_i["op"]
        
        # recursive call to find key
        recurs = {op_key: {key: do_op_from_key(key) if key not in vals else vals[key] for key in [a_key,b_key]}}

        # extract values from keys
        a_i, b_i = vals.get(a_key,None), vals.get(b_key,None)

        # update vals
        vals[out_key] = ops[op_key](a_i,b_i)

        return recurs
    

    wrong_instrs = {}
    i = 0
    while "z45" not in vals:
        # extract keys from index
        x_key, y_key, z_key = f"x{str(i).zfill(2)}", f"y{str(i).zfill(2)}", f"z{str(i).zfill(2)}"
        i+=1

        # do recursive operations to obtain the tree
        operations = do_op_from_key(z_key)
        
        # Operations should form a ripple carry:
        # zi = xi ^ yi ^ ci
        # ci_next = (xi and yi) or (xi ^ yi and ci)

        # if z doesn't have a XOR operation, bad wire
        if operations.get("XOR",None) is None:
            wrong_instrs[z_key] = instructions[z_key]
            continue

        if i>2:
            operands = operations["XOR"]
            for wire_key, op in operands.items():

                # if doesn't apply x_i XOR y_i
                if "XOR" in op: 
                    if x_key not in op["XOR"] or y_key not in op["XOR"]:
                        wrong_instrs[wire_key] = op
                # if inside the OR comparison, don't find 2 AND operators
                elif "OR" in op:
                    for key,val in op["OR"].items():
                        if not "AND" in val:
                            wrong_instrs[key] = val
                # other operation
                else:
                    wrong_instrs[wire_key] = op 
            
    return ",".join(sorted(list(wrong_instrs.keys())))

    

# RUN


file_name = "data/example.txt"
file_name = "data/dec-24.txt"

vals, instructions = load_data(file_name)
# print(vals, instructions)

# out = read_instructions(vals, instructions)
out = read_instrs_with_extra_steps(vals, instructions)
print(out)