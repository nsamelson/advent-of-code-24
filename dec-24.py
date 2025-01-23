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
        return {key:val for key, val in values.items() if key.startswith(letter)}
    
    def get_int(wires):
        return int("".join(
            str(wires[key]) 
            for key in sorted((k for k in wires), reverse=True)
        ),2)
    
    def ripple_carry(a,b,c_in):
        z = a ^ b ^ c_in
        c_out = (a and b) or (a ^ b and c_in)

        return z, c_out
    
    # create lists for z and c
    z_bits = []
    c_bits = [0]

    # get init x and y
    x_wires, y_wires = get_wires("x",vals), get_wires("y", vals)

    # build the solution first (z_comp)
    for i in range(len(x_wires.keys())+1):
        x,y = f"x{str(i).zfill(2)}", f"y{str(i).zfill(2)}"
        c_in = c_bits[i]

        if x_wires.get(x,None) is None:
            z_bits.append(c_in)


        z, c_out = ripple_carry(x_wires[x],y_wires[y],c_in)
        z_bits.append(z)
        c_bits.append(c_out)

    # this idea is to create the z with carry over BEFORE running the instructions
    # then during the instructions read, detect the anomalies (differences between the instr and the real z and c)
    # if there is an anomaly, add back into the queue, then try to swap the outputs? or just manually?


    # x,y = get_int(x_wires), get_int(y_wires)
    # # get z to achieve
    # z_bin = bin(x + y)
    # z_wires = {f"z{str(i).zfill(2)}":int(val) for i,val in enumerate(reversed(list(z_bin)[2:]))}











    # operate instructions
    while instructions:
        instr = instructions.pop(0)

        # extract from instruction
        a_pos, b_pos = instr["in"][0], instr["in"][2]
        op = ops[instr["in"][1]]

        # get bit values
        a = vals.get(a_pos,None)
        b = vals.get(b_pos,None)  

        # if one of them is none, add back to queue
        if a is None or b is None:
            instructions.append(instr)
            continue
        
        # if working with x and y and know carry_bit, then compute 
        if a_pos[1:] == b_pos[1:]:
            bit_pos = a_pos[1:]
            c_in = carry_bits.get(int(bit_pos),None)

            # if no carry bit yet, add to queue
            if c_in is None:
                instructions.append(instr)
                continue

            z_out, c_out = ripple_carry(a,b,c_in)
            # carry_bits[int(bit_pos)+1] = c_out
            # z_comp[int(bit_pos)] = z_out
    

        # run operation and save the value
        vals[instr["out"]] = op(a,b)
        # print(a,b, instr["out"])

    # adding the carrying bit
    last_pos = sorted(z_comp.keys())[-1]
    z_comp[last_pos+1] = carry_bits.get(last_pos+1,0)

    # print(x_wires, y_wires)
    print(z_wires.values())
    print(get_wires("z",vals).values())
    print(z_comp.values())
    print(get_int(z_wires),get_int(get_wires("z",vals)))
    
    




    

    



# RUN


file_name = "data/example.txt"
file_name = "data/dec-24.txt"

vals, instructions = load_data(file_name)
# print(vals, instructions)

# out = read_instructions(vals, instructions)
out = read_instrs_with_extra_steps(vals, instructions)
print(out)