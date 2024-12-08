
import numpy as np
from tqdm import tqdm
import itertools

# day 7


def load_data(file_name):
    equations = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            components = line.split(":")
            result = int(components[0])
            values = [int(val) for val in components[1].split(" ")[1:]]
            equations.append((result,values))

    return equations


# Task 1: find the operators
#   - determine which test values could be produced by placing a combination of operators on each line
#   - operators are either + or *
#   - sum the test values that could be made true

def add(a,b):
    return a + b

def product(a,b):
    return a * b

# task 2: add concatenate
def concat(a,b):
    return int(f"{a}{b}")


def find_operators(equations):
    total_calib_result = 0
    operators = [add, product, concat]
    # operators = ["+","*"]

    for result, values in equations:
        
        operator_configs = list(itertools.product(operators, repeat=len(values)-1))

        
        for config in operator_configs:
            calib_result = values[0]

            for i,operator in enumerate(config):
                calib_result = operator(calib_result, values[i+1])

            if calib_result == result:
                total_calib_result += calib_result
                break
    
    return total_calib_result



# RUN

file_name = "data/example.txt"
file_name = "data/dec-7.txt"

equations = load_data(file_name)
count = find_operators(equations)
print(count)