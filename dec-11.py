
import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 11

def load_data(file_name):
    data = []

    with open(file_name, "r") as f:
        line = f.readline()
        data = line.strip().split(" ")

    return data



# task 1:
#   - stones arranged in a line, each with a number
#   - at blink, number changes, or stone splits in 2 which shifts the stones
#   - stones change simulatneousely, according to the first applicable rule:
#       - if number == 0, number = 1 
#       - if number has even digits (1010), splits stone in 2, each with equal digits (10,10)
#       - if none of these 2 rules apply: stone replaced by a new one, multiplied by 2024
# 
#  blink 25 times



def count_stones(data, blinks = 25):

    def change_stones(stones):
        changed_stones = []
        for stone in stones:
            # apply rules
            if stone == "0":
                changed_stones.append("1")
            elif len(stone) % 2 == 0 and len(stone) > 1:
                split_index = int(len(stone)/2)
                first_stone = stone[:split_index]
                second_stone = str(int(stone[split_index:]))
                changed_stones.extend([first_stone,second_stone])
            else:
                new_stone = str(int(stone) * 2024)
                changed_stones.append(new_stone)

        return changed_stones
    
    changed_stones = data.copy()

    for i in tqdm(range(blinks)):
        changed_stones = change_stones(changed_stones)

    return len(changed_stones)
        


# Task 2: OPTIMISE!!!
import threading
import concurrent.futures
from multiprocessing import Pool
from functools import partial
import timeit

def operate_stone(stone):
    stone_div = divmod(len(stone),2)
    # apply rules
    if stone == "0":
        return ["1"]

    elif stone_div[1] == 0:
        split_index = stone_div[0]

        first_stone = stone[:split_index]
        second_stone = str(int(stone[split_index:]))

        return [first_stone,second_stone]
    else:
        return [str(int(stone) * 2024)]
    

def count_stones_opt(data, blinks = 75):
    def change_stones(stones):
        with Pool(processes=None) as pool: 
            return [item for sublist in pool.map(operate_stone, stones) for item in sublist]

    
    changed_stones = data.copy()

    # iterate over blinks
    for i in range(blinks):
        changed_stones = change_stones(changed_stones)

    return len(changed_stones)


# OTHER WAY depth first search

def operate_blinks(stone, blink, max_blink=75):
    count = 0

    # compute stones
    out_stones = operate_stone(stone)
    blink += 1

    # if reach end of depth
    if blink >= max_blink:
        return len(out_stones)
    
    for out_stone in out_stones:
        count += operate_blinks(out_stone, blink, max_blink)

    return count

def count_stones_dfs(data, max_blinks = 75):
    # changed_stones = data.copy()
    tot_count = 0

    with Pool(processes=None) as pool:
        partial_func = partial(operate_blinks, blink=0, max_blink=max_blinks)

        tot_count = sum(pool.map(partial_func,data))
    return tot_count




# OTHER WAY with dict

def count_stones_cnt(data, max_blinks=75):
    # changed_stones = data.copy()

    stones_dict = { stone: data.count(stone) for stone in data}

    for i in tqdm(range(max_blinks)):

        # print(stones_dict)

        stone_items = stones_dict.copy().items()
        for stone, count in stone_items:
            
            # generate new stones
            new_stones = operate_stone(stone)
            
            # add these new stones in the dict
            for new_stone in new_stones:
                if new_stone in stones_dict.keys():
                    stones_dict[new_stone] += count
                else:
                    stones_dict[new_stone] = count

            # remove the count of stones we changed
            stones_dict[stone] -= count

    return sum(stones_dict.values())



# RUN

file_name = "data/example.txt"
file_name = "data/dec-11.txt"


# count = count_stones(data, 25)

def run_1():
    data = load_data(file_name)
    count = count_stones(data,25)
    print(count)

def run_2():
    data = load_data(file_name)
    count = count_stones_dfs(data,25)
    print(count)

def run_3():
    data = load_data(file_name)
    count = count_stones_cnt(data,75)
    print(count)

if __name__ =="__main__":
    # data = load_data(file_name)
    # exec_opt = timeit.timeit(run_1,number=1)
    # exec_dfs = timeit.timeit(run_2,number=1)
    exec_cnt = timeit.timeit(run_3,number=1)
    # print("OPT: ", exec_opt)
    # print("DFS: ",exec_dfs)
    print("CNT: ",exec_cnt)