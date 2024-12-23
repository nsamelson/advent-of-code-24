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

def assembly_instructions(registers, program):
    out = []

    i = 0
    while i < len(program) - 1:

        opcode = program[i]
        operand = program[i+1]
        
        # get combo operand
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
            
        i +=2

    out_txt = ",".join(str(num) for num in out)
    # print(registers)

    return out_txt

# Task 2:
#   - program supposed to output another copy of the program
#   - Register A is corrupted
#   - Need to find new A value so the program copies itself
#   - this means Program input == Program output

def assembly_auto_program(registers, program):
    

    return None



# RUN

file_name = "data/example.txt"
# file_name = "data/dec-17.txt"

registers, program = load_data(file_name)
out = assembly_instructions(registers, program)

out_2 = assembly_auto_program(registers, program)

print(out, out_2)
