import heapq
import math
import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 17 Chronospatia computer

def load_data(file_name):
    registers = {}
    program = None

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()

            if len(line)==0:
                continue

            word_nums = line.split(":")
            word = word_nums[0].split(" ")[-1]

            if word in ["A","B","C"]:
                num = int(word_nums[1])
                registers[word] = num
            else:
                program =  [int(a) for a in word_nums[1].split(",")]
                

        
    return registers, program

# Task 1:
#   - 3-bit computer (0 to 7)
#   - 3 registers A,B and C but not limited to 3 bits
#   - computer knows 8 instructions, each ided by a 3 bit # (opcode)
#   - each instruction reads the 3 bit # after it as an input (operand)
#   - instruction pointer starts at 0, increases by 2 (except when jumps), halts overshoots the program
#   - 2 types of operand (determined by the isntruction) : literal operand is operand itself and combo operand: 0-3 = literal, 4,5,6 = A,B,C
#   - 8 instructions:
#       - adv (opcode 0) = division of A register / by instruction's combo operand ^2, int(result) into A
#       - bxl (opcode 1) = bitwise XOR of B and literal operand, result into B
#       - bst (opcode 2) = combo operand % 8 (keeps 3 lowest bits), result into B
#       - jnz (opcode 3) = nothing if A == 0 else jumps the instruction pointer to literal operand. If jumps, pointer not increased by 2
#       - bxc (opcode 4) = bitwise XOR of B and C, result into B (ignores instr read)
#       - out (opcode 5) = combo operand % 8, and outputs that value (if more than 1 val, seperate by commas)
#       - bdv (opcode 6) == adv bur result into B
#       - cdv (opcode 7) == adv but result into C

# what is it trying to output

def assembly_instructions(registers, program, verbose=False):
    out = []

    i = 0
    while i < len(program) - 1:

        opcode = program[i]
        operand = program[i+1]

        
        
        # get combo operand
        if operand == 7:
            combo = None
        else:
            combo = operand if operand <=3 else registers[list(registers.keys())[operand - 4]]

        match opcode:
        # operate the opcode
            case 0:
                registers["A"] = int(registers["A"] / (2**combo))
            case 1:
                registers["B"] = registers["B"] ^ operand
            case 2:
                registers["B"] = combo % 8
            case 3:
                if registers["A"] != 0:
                    i = operand
                    continue
            case 4:
                registers["B"] = registers["B"] ^ registers["C"] 
            case 5:
                out.extend([combo % 8])
            case 6:
                registers["B"] = int(registers["A"] / (2**combo))
            case 7:
                registers["C"] = int(registers["A"] / (2**combo))
        if verbose:
            print("index:",i, "code and op:", opcode, operand, "out:",out, "A:", registers["A"])
        i +=2    

    return out

# Task 2:
#   - program supposed to output another copy of the program
#   - Register A is corrupted
#   - Need to find new A value so the program copies itself
#   - this means Program input == Program output
from collections import deque


def assembly_auto_program(start_registers, program, verbose = False):
    start_registers["A"] = 0 # setup corruped to 0
    no_residues = {"A":None,"B":None,"C":None}
    queue = deque([(len(program) - 2, program.copy(), start_registers.copy(), no_residues.copy()) ]) # i, output, registers, residues
    
    # get the jumper indices
    jumper = [j for j,val in enumerate(program) if val == 3 and j % 2 == 0][0]

    counter = 0

    while queue:
        i, output, registers, residues = queue.popleft()
        counter +=1

        opcode = program[i]
        operand = program[i+1]

        # jump_index = [val for val in jumpers if program[val+1] == i]
        jump_index = jumper if program[jumper+1] == i else None
        
        # get combo operand
        combo = None if operand == 7 else operand if operand <= 3 else registers[list(registers.keys())[operand - 4]]

        # iters = [0] if opcode in [1,2,3,4,5] else quotients

        # operate the opcode
        # for j in iters:
        # new_reg = registers.copy()
        new_output = list(output)

        range_val = 8 if any(residues.values()) else 1
        
        # j will be the quotients, ranging from 0 to 7
        for j in range(range_val):
            new_reg = registers.copy()
            new_residues = None
            match opcode:
                case 0:
                    res = residues["A"] if residues["A"] else j
                    new_reg["A"] = new_reg["A"] * (2**combo) + res
                case 1:
                    new_reg["B"] = new_reg["B"] ^ operand
                case 2:
                    new_reg["B"] = combo * 8 + new_reg["B"]
                case 3:
                    pass
                case 4:
                    new_reg["B"] = new_reg["B"] ^ new_reg["C"] 
                case 5:
                    if output:
                        residue = new_output.pop()
                        if 3 < operand <7:
                            new_residues = no_residues.copy()
                            new_residues[list(new_reg.keys())[operand - 4]] = residue
                case 6:
                    res = residues["B"] if residues["B"] else j
                    new_reg["A"] = new_reg["B"] * (2**combo) + res
                case 7:
                    res = residues["C"] if residues["C"] else j
                    new_reg["A"] = new_reg["C"] * (2**combo) + res

            if verbose:
                print("index:",i, "code and op:", opcode, operand, "out:",output, "A:", registers["A"])
                if counter >= 100:
                    break

            if len(output) ==0 and i ==0:
                # return
                verif = assembly_instructions(new_reg.copy(), program.copy())
                if verif == program:
                    print("index:",i, "out:",new_output, "A:", new_reg["A"],"verif:",verif)
                    return new_reg

            if new_residues is None:
                new_residues = no_residues.copy()

            # jumps if one correct index
            next_index = jump_index if jump_index else (i - 2)
            
            if next_index >= 0:
                queue.append((next_index, new_output, new_reg, new_residues))    

        if counter >= 10000000:
            print("index:",i, "code and op:", opcode, operand, "out:",output, "A:", registers["A"])
            break
        

    return None



# RUN

file_name = "data/example.txt"
file_name = "data/dec-17.txt"

registers, program = load_data(file_name)

out_2 = assembly_auto_program(registers.copy(), program, verbose=False)
# registers["A"] = out_2
print("--------------------------")
out = assembly_instructions(registers.copy(), program, verbose=False)
out_txt = ",".join(str(num) for num in out)
print(out_2)
print(out_txt)
