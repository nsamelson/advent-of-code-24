import numpy as np
from tqdm import tqdm
import itertools
import re


# DAY 9

def load_data(file_name):
    data = ""

    with open(file_name, "r") as f:
        data = f.readlines()[0].strip()

    return data

# task 1:
#   - disk maps represent layout of files and free space on the disk. 
#       Digits alternate to indicate length of file and length of free space
#   - each file also has an ID number, based on the generated order, before being rearranged
#   - want to move file blocks one at a time, from end to leftmost free space block (until no free space left)
#   - compute the checksum = multiply each of these blocks position with the file ID number


def compute_checksum(data):
    disk_map = list(data)

    expanded_disk = []
    free_space_indices = []
    block_indices = []
    id_tracker = 0

    # expand data
    for i,digit in enumerate(disk_map):
        start_index = len(expanded_disk)

        if i % 2 == 0:
            expanded_disk.extend([id_tracker]* int(digit))
            block_indices.extend([start_index + j for j in range(int(digit))])
            id_tracker +=1
        else:
            expanded_disk.extend(["."]* int(digit))

            free_space_indices.extend([start_index + j for j in range(int(digit))])
    
    # print(free_space_indices)
    # print(block_indices)
    # print(expanded_disk)

    # Squeeze data
    for i,free_index in enumerate(free_space_indices):

        block_index = block_indices[-(i + 1)]

        # break the loop
        if block_index <= free_index:
            break

        expanded_disk[free_index] = expanded_disk[block_index]        
        expanded_disk[block_index] = "."

    # compute checksum
    checksum = 0
    for i,digit in enumerate(expanded_disk):
        if digit == ".":
            break

        checksum += i * int(digit)
    

    return checksum


# task 2:
#   - move whole files instead of blocks
#   - try to move the file whith the highest id first


def move_whole_files(data):
    disk_map = list(data)

    expanded_disk = []
    free_space_indices = []
    block_indices = []
    id_tracker = 0

    # expand data
    for i,digit in enumerate(disk_map):
        start_index = len(expanded_disk)

        if i % 2 == 0:
            expanded_disk.extend([id_tracker]* int(digit))
            block_indices.append([start_index + j for j in range(int(digit))])
            id_tracker +=1
        else:
            expanded_disk.extend(["."]* int(digit))

            if int(digit) != 0:
                free_space_indices.append([start_index + j for j in range(int(digit))])

    # go through each file in reverse order
    for i , block in enumerate(block_indices[::-1]):
        for j, free_block in enumerate(free_space_indices):
            if len(free_block)==0:
                continue
            if block[0] <= free_block[0]:
                break
            
            # if free space left of current place
            if len(free_block) >= len(block):
                new_indices = free_block[:(len(block))]

                # move file
                expanded_disk[new_indices[0]:new_indices[-1]+1] = expanded_disk[block[0]:block[-1]+1]
                expanded_disk[block[0]:block[-1]+1] = ["."]*len(block)

                # print("Moved: ", block, "to ", new_indices)

                # update the free_space
                del free_space_indices[j][0:len(new_indices)]
                break

    checksum = 0
    for i,digit in enumerate(expanded_disk):
        if digit == ".":
            continue
        
        checksum += i * int(digit)
    

    return checksum

# RUN

file_name = "data/example.txt"
file_name = "data/dec-9.txt"

data = load_data(file_name)
checksum = compute_checksum(data)
new_checksum = move_whole_files(data)
print(new_checksum)
